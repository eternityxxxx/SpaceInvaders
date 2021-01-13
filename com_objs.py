from win32com.server import register
from enemy import Enemy


# Регистрация нового COM объекта
# Как я понимаю, далее по progid мы можем стучаться до его методов
register.UseCommandLine(Enemy)
