import uvicorn
from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator

from . import predict 



app = FastAPI()

model_version = {}
with open("/code/app/model_version.py") as file: 
  model_version=file.read()
  model_version=model_version.split('=')[1].strip()

@app.get('/health')
async def index():
  return {"text":"Api is alive", "modeel_version":model_version}


@app.post("/api")
async def api(info : Request):
  data = await info.json()
  experience_level = str(data['experience_level'])
  employment_type = str(data['employment_type'])
  company_size = str(data['company_size'])
  work_year= str(data['work_year'])
  job_title = str(data['job_title'])
  remote_ratio = str(data['remote_ratio'])
  employee_residence = str(data['employee_residence'])

  output = predict.predict(experience_level, employment_type, company_size, work_year, job_title, remote_ratio, employee_residence)
  print(output)
  return output[0]

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)
    
if __name__ == '__main__':
  uvicorn.run(app,host="127.0.0.1",port=8000)
