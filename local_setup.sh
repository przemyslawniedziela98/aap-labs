PROJECT_DIR="$(pwd)"
VENV_DIR="$PROJECT_DIR/venv"
STATIC_DIR="$PROJECT_DIR/app/static"
STATIC_ZIP="$PROJECT_DIR/static.zip"
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"
MIGRATIONS_DIR="$PROJECT_DIR/migrations"

if [ ! -d "$VENV_DIR" ]; then
  echo "Virtual environment not found. Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
  echo "Virtual environment created in $VENV_DIR"
else
  echo "Virtual environment already exists."
fi

source "$VENV_DIR/bin/activate"

if [ -f "$REQUIREMENTS_FILE" ]; then
  echo "Installing dependencies from requirements.txt..."
  pip install -r "$REQUIREMENTS_FILE"
else
  echo "No requirements.txt file found."
fi

if [ ! -d "$MIGRATIONS_DIR" ]; then
  echo "Migrations directory not found. Creating migrations directory..."
  flask db init
else
  echo "Migrations directory already exists."
fi

echo "Setting up logger..."
flask db upgrade

if [ -d "$STATIC_DIR" ]; then
  echo "Static directory found. Unzipping static.zip..."
  if [ -f "$STATIC_ZIP" ]; then
    unzip -o "$STATIC_ZIP" -d "$STATIC_DIR"
    echo "Static files unzipped into $STATIC_DIR"
  else
    echo "Static zip file not found. Please provide a static.zip file."
  fi
else
  echo "Static directory not found. Please create the app/static directory manually."
fi

