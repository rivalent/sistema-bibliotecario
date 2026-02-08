import logging
import traceback
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from src.service.report_service import ReportService

logging.basicConfig(level=logging.DEBUG)
router = APIRouter()
service = ReportService()

@router.get('/reports/expired', status_code=status.HTTP_200_OK)
def get_expired_loans():
    try:
        report_data = service.get_expired_report()
        
        logging.debug(f"[REPORT-API] Found {len(report_data)} expired records")
        return report_data

    except Exception as error:
        logging.error(f"[REPORT-API] Fail to get expired report: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))


@router.get('/reports/available', status_code=status.HTTP_200_OK)
def get_available_books(book_isbn: Optional[str] = None):
    try:
        available_items = service.get_available_books_report(book_isbn)
        
        logging.debug(f"[REPORT-API] Found {len(available_items)} available items")
        return available_items

    except Exception as error:
        logging.error(f"[REPORT-API] Fail to get available report: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))


@router.get('/reports/taken', status_code=status.HTTP_200_OK)
def get_taken_books():
    try:
        taken_items = service.get_taken_books_report()
        
        logging.debug(f"[REPORT-API] Found {len(taken_items)} items currently taken")
        return taken_items

    except Exception as error:
        logging.error(f"[REPORT-API] Fail to get taken report: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))
