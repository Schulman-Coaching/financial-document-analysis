#!/usr/bin/env python3
"""
Google Drive Document Management System for Family Law Practice
Connects to Google Drive to manage case documents, financial records, and legal filings
"""

import os
import json
import pickle
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
import hashlib
import mimetypes
import re

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

# For document processing
import PyPDF2
from docx import Document
import io

@dataclass
class CaseMetadata:
    """Metadata for family law cases"""
    case_id: str
    client_name: str
    opposing_party: str
    case_type: str  # divorce, custody, support, etc.
    jurisdiction: str
    filing_date: str
    status: str
    attorney_assigned: str
    paralegal_assigned: str
    tags: List[str] = field(default_factory=list)
    
@dataclass
class DocumentMetadata:
    """Metadata for individual documents"""
    document_id: str
    case_id: str
    document_type: str  # pleading, financial, correspondence, evidence, etc.
    document_name: str
    file_path: str
    file_size: int
    created_date: str
    modified_date: str
    uploaded_by: str
    description: str = ""
    keywords: List[str] = field(default_factory=list)
    confidential: bool = False
    version: int = 1
    related_documents: List[str] = field(default_factory=list)
    
@dataclass
class DriveFolderStructure:
    """Standard folder structure for family law practice"""
    root_folder_id: str
    folders: Dict[str, str]  # folder_name: folder_id
    
class FamilyLawDriveManager:
    """Main class for managing Google Drive integration for family law practice"""
    
    # Define scopes for Google Drive API
    SCOPES = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive.appdata',
        'https://www.googleapis.com/auth/drive.metadata'
    ]
    
    # Standard folder structure for family law practice
    STANDARD_FOLDERS = [
        "1_Case Files",
        "2_Financial Documents",
        "3_Court Filings",
        "4_Correspondence",
        "5_Evidence",
        "6_Research",
        "7_Templates",
        "8_Administrative"
    ]
    
    # Document categories with subfolders
    DOCUMENT_CATEGORIES = {
        "pleadings": [
            "Complaints",
            "Answers",
            "Motions",
            "Orders to Show Cause",
            "Responsive Papers",
            "Stipulations",
            "Judgments"
        ],
        "financial": [
            "Net Worth Statements",
            "Tax Returns",
            "Bank Statements",
            "Pay Stubs",
            "Business Records",
            "Retirement Accounts",
            "Real Estate Documents"
        ],
        "discovery": [
            "Demands",
            "Responses",
            "Interrogatories",
            "Document Production",
            "Subpoenas",
            "Depositions"
        ],
        "correspondence": [
            "Client Letters",
            "Opposing Counsel",
            "Court Correspondence",
            "Expert Correspondence"
        ],
        "evidence": [
            "Photographs",
            "Emails",
            "Text Messages",
            "Social Media",
            "Audio Recordings",
            "Video Recordings"
        ]
    }
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.root_folder_id = None
        self.folder_structure = None
        self.case_index = {}  # case_id: CaseMetadata
        self.document_index = {}  # document_id: DocumentMetadata
        
    def authenticate(self) -> bool:
        """Authenticate with Google Drive API"""
        creds = None
        
        # Check for existing token
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as token:
                    creds_data = json.load(token)
                    creds = Credentials.from_authorized_user_info(creds_data, self.SCOPES)
            except Exception as e:
                print(f"Error loading token: {e}")
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token: {e}")
                    creds = None
            
            if not creds:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Error during authentication: {e}")
                    return False
            
            # Save credentials
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        try:
            self.service = build('drive', 'v3', credentials=creds)
            return True
        except Exception as e:
            print(f"Error building Drive service: {e}")
            return False
    
    def initialize_drive_structure(self, root_folder_name: str = "Family Law Practice") -> bool:
        """Initialize the standard folder structure in Google Drive"""
        if not self.service:
            return False
        
        try:
            # Create or find root folder
            query = f"name='{root_folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                self.root_folder_id = folders[0]['id']
                print(f"Found existing root folder: {root_folder_name}")
            else:
                # Create root folder
                file_metadata = {
                    'name': root_folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.service.files().create(
                    body=file_metadata,
                    fields='id'
                ).execute()
                self.root_folder_id = folder.get('id')
                print(f"Created new root folder: {root_folder_name}")
            
            # Create standard folders
            self.folder_structure = DriveFolderStructure(
                root_folder_id=self.root_folder_id,
                folders={}
            )
            
            for folder_name in self.STANDARD_FOLDERS:
                folder_id = self._create_folder(folder_name, self.root_folder_id)
                if folder_id:
                    self.folder_structure.folders[folder_name] = folder_id
            
            # Create template subfolders
            templates_folder_id = self.folder_structure.folders.get("7_Templates")
            if templates_folder_id:
                for category, subfolders in self.DOCUMENT_CATEGORIES.items():
                    category_folder_id = self._create_folder(category.title(), templates_folder_id)
                    if category_folder_id:
                        for subfolder in subfolders:
                            self._create_folder(subfolder, category_folder_id)
            
            print("Drive structure initialized successfully")
            return True
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
    
    def _create_folder(self, folder_name: str, parent_id: str = None) -> Optional[str]:
        """Create a folder in Google Drive"""
        try:
            # Check if folder already exists
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            if parent_id:
                query += f" and '{parent_id}' in parents"
            
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            folders = results.get('files', [])
            if folders:
                return folders[0]['id']
            
            # Create new folder
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            return folder.get('id')
        except HttpError as error:
            print(f"Error creating folder {folder_name}: {error}")
            return None
    
    def create_case_folder(self, case_metadata: CaseMetadata) -> Optional[str]:
        """Create a folder structure for a new case"""
        if not self.service or not self.folder_structure:
            return None
        
        try:
            # Create main case folder
            case_folder_name = f"{case_metadata.case_id} - {case_metadata.client_name}"
            case_folder_id = self._create_folder(
                case_folder_name,
                self.folder_structure.folders.get("1_Case Files")
            )
            
            if not case_folder_id:
                return None
            
            # Create subfolders
            subfolders = [
                "01_Pleadings",
                "02_Financial_Disclosure",
                "03_Discovery",
                "04_Correspondence",
                "05_Evidence",
                "06_Research",
                "07_Court_Filings",
                "08_Billing"
            ]
            
            for subfolder in subfolders:
                self._create_folder(subfolder, case_folder_id)
            
            # Store case metadata
            self.case_index[case_metadata.case_id] = case_metadata
            
            # Save metadata
            self._save_document_index()
            
            print(f"Created case folder: {case_folder_name}")
            return case_folder_id
            
        except HttpError as error:
            print(f"Error creating case folder: {error}")
            return None
    
    def upload_document(self, 
                       file_path: str,
                       case_id: str,
                       document_type: str,
                       description: str = "",
                       confidential: bool = False,
                       keywords: List[str] = None) -> Optional[DocumentMetadata]:
        """Upload a document to the appropriate case folder"""
        if not self.service:
            return None
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None
        
        try:
            # Get case information
            case_metadata = self.case_index.get(case_id)
            if not case_metadata:
                print(f"Case {case_id} not found in index")
                return None
            
            # Find case folder
            case_folder_id = self._find_case_folder(case_id)
            if not case_folder_id:
                print(f"Case folder not found for case {case_id}")
                return None
            
            # Determine target folder based on document type
            target_folder_id = self._get_target_folder(case_folder_id, document_type)
            
            # Generate document ID
            document_id = self._generate_document_id(case_id, document_type, file_path)
            
            # Prepare file metadata
            file_metadata = {
                'name': os.path.basename(file_path),
                'parents': [target_folder_id],
                'description': description,
                'appProperties': {
                    'case_id': case_id,
                    'document_type': document_type,
                    'confidential': str(confidential),
                    'upload_timestamp': datetime.now().isoformat()
                }
            }
            
            # Upload file
            mime_type, _ = mimetypes.guess_type(file_path)
            media = MediaFileUpload(
                file_path,
                mimetype=mime_type,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, size, createdTime, modifiedTime'
            ).execute()
            
            # Create document metadata
            document_metadata = DocumentMetadata(
                document_id=document_id,
                case_id=case_id,
                document_type=document_type,
                document_name=os.path.basename(file_path),
                file_path=file_path,
                file_size=int(file.get('size', 0)),
                created_date=file.get('createdTime', ''),
                modified_date=file.get('modifiedTime', ''),
                uploaded_by='system',
                description=description,
                keywords=keywords or [],
                confidential=confidential,
                version=1
            )
            
            # Store in index
            self.document_index[document_id] = document_metadata
            
            # Save metadata
            self._save_document_index()
            
            print(f"Uploaded document: {document_metadata.document_name}")
            return document_metadata
            
        except HttpError as error:
            print(f"An error occurred during upload: {error}")
            return None
        except Exception as e:
            print(f"Error uploading document: {e}")
            return None
    
    def _find_case_folder(self, case_id: str) -> Optional[str]:
        """Find the folder ID for a specific case"""
        try:
            case_metadata = self.case_index.get(case_id)
            if not case_metadata:
                return None
            
            case_folder_name = f"{case_metadata.case_id} - {case_metadata.client_name}"
            
            query = (f"name='{case_folder_name}' and "
                    f"'{self.folder_structure.folders.get('1_Case Files')}' in parents and "
                    f"mimeType='application/vnd.google-apps.folder' and "
                    f"trashed=false")
            
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            folders = results.get('files', [])
            return folders[0]['id'] if folders else None
            
        except Exception as e:
            print(f"Error finding case folder: {e}")
            return None
    
    def _get_target_folder(self, case_folder_id: str, document_type: str) -> str:
        """Determine the appropriate subfolder for a document type"""
        folder_mapping = {
            'complaint': '01_Pleadings',
            'answer': '01_Pleadings',
            'motion': '01_Pleadings',
            'osc': '01_Pleadings',
            'net_worth': '02_Financial_Disclosure',
            'tax_return': '02_Financial_Disclosure',
            'bank_statement': '02_Financial_Disclosure',
            'pay_stub': '02_Financial_Disclosure',
            'interrogatory': '03_Discovery',
            'document_production': '03_Discovery',
            'subpoena': '03_Discovery',
            'deposition': '03_Discovery',
            'letter': '04_Correspondence',
            'email': '04_Correspondence',
            'photo': '05_Evidence',
            'text_message': '05_Evidence',
            'social_media': '05_Evidence',
            'court_filing': '07_Court_Filings'
        }
        
        subfolder_name = folder_mapping.get(document_type, '01_Pleadings')
        
        # Find or create subfolder
        query = (f"name='{subfolder_name}' and "
                f"'{case_folder_id}' in parents and "
                f"mimeType='application/vnd.google-apps.folder' and "
                f"trashed=false")
        
        try:
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            folders = results.get('files', [])
            if folders:
                return folders[0]['id']
            else:
                return self._create_folder(subfolder_name, case_folder_id)
                
        except Exception as e:
            print(f"Error getting target folder: {e}")
            return case_folder_id
    
    def _generate_document_id(self, case_id: str, doc_type: str, file_path: str) -> str:
        """Generate a unique document ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_hash = hashlib.md5(f"{case_id}_{doc_type}_{os.path.basename(file_path)}".encode()).hexdigest()[:8]
        return f"DOC-{case_id}-{doc_type}-{file_hash}-{timestamp}"
    
    def search_documents(self, 
                        query: str,
                        case_id: str = None,
                        document_type: str = None,
                        date_range: Tuple[str, str] = None) -> List[DocumentMetadata]:
        """Search for documents based on various criteria"""
        results = []
        
        for doc_id, metadata in self.document_index.items():
            if case_id and metadata.case_id != case_id:
                continue
            
            if document_type and metadata.document_type != document_type:
                continue
            
            if date_range:
                doc_date = datetime.fromisoformat(metadata.created_date.replace('Z', '+00:00'))
                start_date = datetime.fromisoformat(date_range[0])
                end_date = datetime.fromisoformat(date_range[1])
                
                if not (start_date <= doc_date <= end_date):
                    continue
            
            search_text = f"{metadata.document_name} {metadata.description} {' '.join(metadata.keywords)}".lower()
            if query.lower() in search_text:
                results.append(metadata)
        
        return results
    
    def get_case_documents(self, case_id: str) -> List[DocumentMetadata]:
        """Get all documents for a specific case"""
        return [doc for doc in self.document_index.values() if doc.case_id == case_id]
    
    def _save_document_index(self):
        """Save document index to local file"""
        try:
            index_data = {
                'documents': {doc_id: asdict(metadata) 
                            for doc_id, metadata in self.document_index.items()},
                'cases': {case_id: asdict(metadata) 
                         for case_id, metadata in self.case_index.items()},
                'timestamp': datetime.now().isoformat()
            }
            
            with open('drive_index.json', 'w') as f:
                json.dump(index_data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving document index: {e}")
    
    def _load_document_index(self):
        """Load document index from local file"""
        try:
            if os.path.exists('drive_index.json'):
                with open('drive_index.json', 'r') as f:
                    index_data = json.load(f)
                
                self.document_index = {
                    doc_id: DocumentMetadata(**metadata)
                    for doc_id, metadata in index_data.get('documents', {}).items()
                }
                
                self.case_index = {
                    case_id: CaseMetadata(**metadata)
                    for case_id, metadata in index_data.get('cases', {}).items()
                }
                
        except Exception as e:
            print(f"Error loading document index: {e}")
    
    def generate_case_report(self, case_id: str) -> Optional[Dict]:
        """Generate a report of all documents in a case"""
        case_metadata = self.case_index.get(case_id)
        if not case_metadata:
            return None
        
        case_docs = self.get_case_documents(case_id)
        
        categorized_docs = {}
        for doc in case_docs:
            if doc.document_type not in categorized_docs:
                categorized_docs[doc.document_type] = []
            categorized_docs[doc.document_type].append(asdict(doc))
        
        report = {
            'case_info': asdict(case_metadata),
            'document_summary': {
                'total_documents': len(case_docs),
                'by_type': {doc_type: len(docs) 
                           for doc_type, docs in categorized_docs.items()},
                'total_size_mb': sum(doc.file_size for doc in case_docs) / (1024 * 1024)
            },
            'documents_by_type': categorized_docs,
            'generated_date': datetime.now().isoformat()
        }
        
        return report
