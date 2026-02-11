import logging
import traceback
from fastapi import APIRouter, HTTPException, status
from src.service.loan_service import LoanService
from src.schemas.loan_schema import RentRequest, ReturnRequest

logging.basicConfig(level=logging.DEBUG)
router = APIRouter()
service = LoanService()

@router.post('/loans', status_code=status.HTTP_201_CREATED)
def create_loan(loan_data: RentRequest):
    try:
        new_loan = service.rent_book(
            user_id=loan_data.user_id,
            portfolio_id=loan_data.portfolio_id,
            days=loan_data.days
        )

        if not new_loan:
             raise HTTPException(status_code=400, detail="Failed to rent. Check if User/Portfolio exists and is available.")

        logging.debug(f"[LOAN-API] Created successfully: {new_loan.id}")
        return new_loan.to_dict()
    
    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[LOAN-API] Fail to create: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))

@router.patch('/loans/{loan_id}/return', status_code=status.HTTP_200_OK)
def return_book(loan_id: str, return_data: ReturnRequest):
    try:
        success = service.return_book(
            loan_id=loan_id,
            return_condition_str=return_data.condition_enum.strip().lower() 
        )

        if not success:
            logging.debug(f"[LOAN-API] Return failed for Loan {loan_id}")
            raise HTTPException(status_code=404, detail="Loan not found, already returned, or invalid Condition Enum")

        logging.debug(f"[LOAN-API] Book returned successfully: {loan_id}")
        return {"message": "Book returned successfully"} 

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[LOAN-API] Fail to return: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))

@router.get('/loans/my-loans/{user_id}', status_code=status.HTTP_200_OK)
def get_my_loans(user_id: str): 
    try:
        loans = service.get_my_loans(user_id)

        logging.debug(f"[LOAN-API] Found {len(loans)} active loans for user {user_id}")
        return [loan.to_dict() for loan in loans]

    except Exception as error:
        logging.error(f"[LOAN-API] Fail to get: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))
