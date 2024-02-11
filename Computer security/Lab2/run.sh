chmod u+x user_managment.py
chmod u+x login.py
echo "Adding user blaz"
./user_managment.py add blaz
echo "Enter password for blaz"

echo "Removing user blaz"
./user_managment.py del blaz

echo "Force password change for user blaz"
./user_managment.py forcepass blaz

echo "Change password for user blaz"
./user_managment.py password blaz

echo "Login as user blaz"
./login.py blaz