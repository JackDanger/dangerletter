FROM public.ecr.aws/lambda/python:latest-arm64

COPY requirements.txt .
COPY *.py ${LAMBDA_TASK_ROOT}/

RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"


CMD [ "app.handler" ]