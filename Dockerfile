# ---- Stage 1: Build Environment ----
FROM python:3.12-slim-trixie AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY image-requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ---- Stage 2: Runtime Environment ----
FROM python:3.12-slim-trixie
RUN addgroup --system app && adduser --system --group app
WORKDIR /home/app
COPY --from=builder /opt/venv /opt/venv
COPY app.py .
RUN chown -R app:app /home/app
ENV PATH="/opt/venv/bin:$PATH"

# Set the default readiness time
ENV READINESS_TIME=30
ENV DB_PASSWORD="insecure_password"

USER app
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]