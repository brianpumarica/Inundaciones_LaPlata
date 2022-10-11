# Grupo 29

## Integrantes

Brian Pumarica 14401/0  
Fiorella Valente 14698/4  
Karim Emilio 15498/1  
Sofia Sotomayor 14641/5

## Base de datos

En schema.sql hay un dump para la base de datos.

La nomenclatura de las tablas es en *inglés*:
- users
- user_roles
- roles_permissions
- permissions
- locations (puntos de encuentro)
- routes (recorridos de evacuación)
- complaints (denuncias)
- config (configuración)

## Roles

Existen dos roles en el sistema:

- Rol Administrador
- Rol Operador

Ejemplo de rol *únicamente* administrador:

- Usuario: lucas@gmail.com
- Contraseña: 123

Ejemplo de rol *únicamente* operador:

- Usuario: pedro@gmail.com
- Contraseña: 123

Ejemplo de rol administrador y operador:

- Usuario: juan@gmail.com
- Contraseña: 123

## Módulos (aplicación privada)

### Módulo de sesión

- Login de usuarios
- Logout de usuarios

### Módulo de usuarios

- Listado de usuarios
- Alta de usuarios
- Baja de usuarios
- Modificación de usuarios
- Activación/desactivación de usuarios
- Búsqueda y filtrado de usuarios

## Módulo de configuración

- Modificación y visualización de la cantidad de elementos por página en los listados del sistema
- Modificación y visualización del criterio de ordenación por defecto de los listados (ascendente o descendente)
- Modificación y visualización de la paleta de colores de la aplicación privada (3 colores)
- Modificación y visualización de la paleta de colores de la aplicación pública (3 colores)

## Módulo de puntos de encuentro

- Listado de puntos de encuentro
- Alta de puntos de encuentro
- Baja de puntos de encuentro
- Vista de detalle de puntos de encuentro
- Modificación de puntos de encuentro
- Publicación/des-publicación de puntos de encuentro
- Búsqueda y filtrado de puntos de encuentro