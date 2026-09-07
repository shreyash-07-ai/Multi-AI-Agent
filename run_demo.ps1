Write-Host "Starting FastAPI..."
Start-Process powershell -ArgumentList "-NoExit","-Command",".\.venv\Scripts\activate; uvicorn app.main:app --reload --port 8000"
Start-Sleep -Seconds 2
Write-Host "Starting Streamlit..."
Start-Process powershell -ArgumentList "-NoExit","-Command",".\.venv\Scripts\activate; streamlit run frontend/app.py"
Write-Host "Open the Streamlit URL shown in the new terminal."
