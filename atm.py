from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from supabase import create_client

SUPABASE_URL = "https://abostfpuhcecmfbknafx.supabase.co"
SUPABASE_KEY = "sb_publishable_9YhEQjcy63_1TA1o8GSmbw_GYHZuuOu" 

db = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Bank Manager API")


@app.get("/accounts")
def get_all_accounts():
    try:
        result = db.table("account").select("*").execute()
        return JSONResponse(content=result.data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/transactions")
def get_all_transactions():
    try:
        result = db.table("transaction").select("*").execute()
        return JSONResponse(content=result.data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/transaction")
def transfer_money(source: str, dest: str, amount: int):

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    # Source account
    src = db.table("account").select("balance").eq(
        "account_number", source
    ).execute()

    if not src.data:
        raise HTTPException(status_code=404, detail="Source account not found")

    src_balance = src.data[0]["balance"]

    if src_balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Destination account
    dest_acc = db.table("account").select("balance").eq(
        "account_number", dest
    ).execute()

    if not dest_acc.data:
        raise HTTPException(status_code=404, detail="Destination account not found")

    dest_balance = dest_acc.data[0]["balance"]

    # Update balances
    db.table("account").update(
        {"balance": src_balance - amount}
    ).eq("account_number", source).execute()

    db.table("account").update(
        {"balance": dest_balance + amount}
    ).eq("account_number", dest).execute()

    # Insert transactions
    db.table("transaction").insert({
        "account_number": source,
        "amount": amount,
        "type": "debit"
    }).execute()

    db.table("transaction").insert({
        "account_number": dest,
        "amount": amount,
        "type": "credit"
    }).execute()

    return JSONResponse(content={"message": "Transfer successful"})
