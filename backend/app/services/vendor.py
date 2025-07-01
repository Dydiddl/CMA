#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
거래처 서비스 모듈
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Tuple
from ..models.vendor import Vendor, VendorDocument
from ..schemas.vendor import VendorCreate, VendorUpdate, VendorDocumentCreate, VendorResponse, VendorListResponse
from ..core.exceptions import ValidationException


class VendorService:
    """거래처 서비스 클래스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_vendor(self, vendor: VendorCreate) -> VendorResponse:
        """새로운 거래처를 등록합니다."""
        try:
            db_vendor = Vendor(**vendor.dict())
            self.db.add(db_vendor)
            self.db.commit()
            self.db.refresh(db_vendor)
            
            return VendorResponse(
                id=db_vendor.id,
                name=db_vendor.name,
                business_number=db_vendor.business_number,
                representative=db_vendor.representative,
                address=db_vendor.address,
                phone=db_vendor.phone,
                email=db_vendor.email,
                bank_name=db_vendor.bank_name,
                bank_account=db_vendor.bank_account,
                status=db_vendor.status,
                description=db_vendor.description,
                created_at=db_vendor.created_at,
                updated_at=db_vendor.updated_at,
                documents=[]
            )
        except IntegrityError:
            self.db.rollback()
            raise ValidationException("이미 존재하는 거래처입니다.")
        except Exception as e:
            self.db.rollback()
            raise ValidationException(f"거래처 생성 중 오류 발생: {e}")
    
    def get_vendors(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[VendorResponse], int]:
        """거래처 목록을 조회합니다."""
        try:
            query = self.db.query(Vendor)
            
            if status:
                query = query.filter(Vendor.status == status)
            
            if search:
                query = query.filter(
                    Vendor.name.contains(search) |
                    Vendor.business_number.contains(search) |
                    Vendor.representative.contains(search)
                )
            
            total = query.count()
            vendors = query.offset(skip).limit(limit).all()
            
            vendor_responses = [
                VendorResponse(
                    id=vendor.id,
                    name=vendor.name,
                    business_number=vendor.business_number,
                    representative=vendor.representative,
                    address=vendor.address,
                    phone=vendor.phone,
                    email=vendor.email,
                    bank_name=vendor.bank_name,
                    bank_account=vendor.bank_account,
                    status=vendor.status,
                    description=vendor.description,
                    created_at=vendor.created_at,
                    updated_at=vendor.updated_at,
                    documents=[]
                ) for vendor in vendors
            ]
            
            return vendor_responses, total
            
        except Exception as e:
            raise ValidationException(f"거래처 목록 조회 중 오류 발생: {e}")
    
    def get_vendor(self, vendor_id: int) -> Optional[VendorResponse]:
        """특정 거래처의 정보를 조회합니다."""
        try:
            vendor = self.db.query(Vendor).filter(Vendor.id == vendor_id).first()
            
            if not vendor:
                return None
            
            return VendorResponse(
                id=vendor.id,
                name=vendor.name,
                business_number=vendor.business_number,
                representative=vendor.representative,
                address=vendor.address,
                phone=vendor.phone,
                email=vendor.email,
                bank_name=vendor.bank_name,
                bank_account=vendor.bank_account,
                status=vendor.status,
                description=vendor.description,
                created_at=vendor.created_at,
                updated_at=vendor.updated_at,
                documents=[]
            )
            
        except Exception as e:
            raise ValidationException(f"거래처 조회 중 오류 발생: {e}")
    
    def update_vendor(
        self,
        vendor_id: int,
        vendor: VendorUpdate
    ) -> Optional[VendorResponse]:
        """거래처 정보를 업데이트합니다."""
        try:
            db_vendor = self.db.query(Vendor).filter(Vendor.id == vendor_id).first()
            
            if not db_vendor:
                return None
            
            for key, value in vendor.dict(exclude_unset=True).items():
                setattr(db_vendor, key, value)
            
            self.db.commit()
            self.db.refresh(db_vendor)
            
            return VendorResponse(
                id=db_vendor.id,
                name=db_vendor.name,
                business_number=db_vendor.business_number,
                representative=db_vendor.representative,
                address=db_vendor.address,
                phone=db_vendor.phone,
                email=db_vendor.email,
                bank_name=db_vendor.bank_name,
                bank_account=db_vendor.bank_account,
                status=db_vendor.status,
                description=db_vendor.description,
                created_at=db_vendor.created_at,
                updated_at=db_vendor.updated_at,
                documents=[]
            )
            
        except IntegrityError:
            self.db.rollback()
            raise ValidationException("이미 존재하는 거래처입니다.")
        except Exception as e:
            self.db.rollback()
            raise ValidationException(f"거래처 수정 중 오류 발생: {e}")
    
    def delete_vendor(self, vendor_id: int) -> bool:
        """거래처를 삭제합니다."""
        try:
            db_vendor = self.db.query(Vendor).filter(Vendor.id == vendor_id).first()
            
            if not db_vendor:
                return False
            
            self.db.delete(db_vendor)
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise ValidationException(f"거래처 삭제 중 오류 발생: {e}")
    
    def create_vendor_document(
        self,
        vendor_id: int,
        document: VendorDocumentCreate
    ) -> VendorDocument:
        """거래처 문서를 생성합니다."""
        try:
            db_document = VendorDocument(**document.dict(), vendor_id=vendor_id)
            self.db.add(db_document)
            self.db.commit()
            self.db.refresh(db_document)
            return db_document
            
        except Exception as e:
            self.db.rollback()
            raise ValidationException(f"거래처 문서 생성 중 오류 발생: {e}")
    
    def get_vendor_documents(
        self,
        vendor_id: int
    ) -> List[VendorDocument]:
        """거래처의 모든 문서를 조회합니다."""
        try:
            return self.db.query(VendorDocument).filter(
                VendorDocument.vendor_id == vendor_id
            ).all()
            
        except Exception as e:
            raise ValidationException(f"거래처 문서 조회 중 오류 발생: {e}") 