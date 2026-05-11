FROM python:3.9

# Jańa paydalanıshı jaratamız (Hugging Face talabı)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Kitapxanalardı ornatıw
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Barlıq fayllardı (main.py, index.html h.t.b) serverge kóshiriw
COPY --chown=user . /app

# Hugging Face ushın 7860-portta serverdi iske túsiriw
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]