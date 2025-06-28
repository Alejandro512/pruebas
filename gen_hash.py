import bcrypt

# Cambia por la contraseña real
plain_password = "LaboratorioATA@5202"

# Genera salt con 12 rondas
salt = bcrypt.gensalt(rounds=12)

# Genera hash usando ese salt
hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)

print("Salt:", salt.decode())
print("Password Hash:", hashed.decode())
