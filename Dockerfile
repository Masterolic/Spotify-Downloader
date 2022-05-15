FROM archlinux/archlinux:latest

# Install the base packages and any dependencies
RUN pacman -Syu --noconfirm && pacman -S --noconfirm python-pip git

# Changing the working directory
WORKDIR /app

# Copy the requirements.txt file into working directory and install the packages
COPY requirements.txt .
RUN pip3 install -U -r requirements.txt

# Copy all the files into working directory
COPY . .

CMD ["python3", "-m", "mbot"]
