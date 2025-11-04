USE workhub_db;

CREATE TABLE Sedes (
    id_sede INT AUTO_INCREMENT PRIMARY KEY,
    nombre_sede VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(20)
) ENGINE=InnoDB;

CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(150) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('SuperAdmin', 'Admin', 'Coordinador') NOT NULL,
    id_sede_asignada INT,
    FOREIGN KEY (id_sede_asignada) REFERENCES Sedes(id_sede) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE Planes (
    id_plan INT AUTO_INCREMENT PRIMARY KEY,
    nombre_plan VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    beneficios TEXT,
    creditos_reserva_mes INT DEFAULT 0
) ENGINE=InnoDB;

CREATE TABLE Miembros (
    id_miembro INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(150) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    datos_facturacion TEXT,
    fecha_registro DATE NOT NULL,
    estado ENUM('Activo', 'Suspendido', 'Inactivo') DEFAULT 'Activo',
    foto_perfil_path VARCHAR(255), -- Requisito PILLOW
    id_plan INT NOT NULL,
    id_sede INT NOT NULL,
    FOREIGN KEY (id_plan) REFERENCES Planes(id_plan) ON DELETE RESTRICT,
    FOREIGN KEY (id_sede) REFERENCES Sedes(id_sede) ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE Espacios (
    id_espacio INT AUTO_INCREMENT PRIMARY KEY,
    nombre_espacio VARCHAR(100) NOT NULL,
    tipo ENUM('Sala Reunión', 'Cabina', 'Salon Evento', 'Otro') NOT NULL,
    capacidad INT,
    id_sede INT NOT NULL,
    FOREIGN KEY (id_sede) REFERENCES Sedes(id_sede) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_miembro INT NOT NULL,
    id_espacio INT NOT NULL,
    fecha_hora_inicio DATETIME NOT NULL,
    fecha_hora_fin DATETIME NOT NULL,
    estado ENUM('Confirmada', 'Pendiente', 'Cancelada') DEFAULT 'Confirmada',
    FOREIGN KEY (id_miembro) REFERENCES Miembros(id_miembro) ON DELETE CASCADE,
    FOREIGN KEY (id_espacio) REFERENCES Espacios(id_espacio) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_miembro INT NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    fecha_emision DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    estado_pago ENUM('Pendiente', 'Pagada', 'Vencida') DEFAULT 'Pendiente',
    descripcion TEXT,
    FOREIGN KEY (id_miembro) REFERENCES Miembros(id_miembro) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Tickets_Soporte (
    id_ticket INT AUTO_INCREMENT PRIMARY KEY,
    id_miembro_reporta INT NOT NULL,
    id_usuario_asignado INT,
    asunto VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('Abierto', 'En Progreso', 'Resuelto', 'Escalado') DEFAULT 'Abierto',
    prioridad ENUM('Baja', 'Media', 'Alta') DEFAULT 'Baja',
    FOREIGN KEY (id_miembro_reporta) REFERENCES Miembros(id_miembro),
    FOREIGN KEY (id_usuario_asignado) REFERENCES Usuarios(id_usuario)
) ENGINE=InnoDB;

CREATE TABLE Eventos (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    fecha_evento DATETIME NOT NULL,
    lugar VARCHAR(255),
    imagen_evento_path VARCHAR(255), -- Requisito Form 2 con Imagen
    id_sede INT NOT NULL,
    FOREIGN KEY (id_sede) REFERENCES Sedes(id_sede) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Eventos_RSVP (
    id_rsvp INT AUTO_INCREMENT PRIMARY KEY,
    id_evento INT NOT NULL,
    id_miembro INT NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_evento) REFERENCES Eventos(id_evento) ON DELETE CASCADE,
    FOREIGN KEY (id_miembro) REFERENCES Miembros(id_miembro) ON DELETE CASCADE,
    UNIQUE(id_evento, id_miembro)
) ENGINE=InnoDB;

CREATE TABLE Anuncios (
    id_anuncio INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    contenido TEXT NOT NULL,
    fecha_publicacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_usuario_publica INT NOT NULL,
    id_sede INT NOT NULL,
    FOREIGN KEY (id_usuario_publica) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_sede) REFERENCES Sedes(id_sede) ON DELETE CASCADE
) ENGINE=InnoDB;

-- --- DATOS DE EJEMPLO ---
-- (Importante: Las contraseñas 'admin123' y 'super123' se hashearán desde la app)
INSERT INTO Sedes (nombre_sede, direccion, telefono)
VALUES ('Sede Central Envigado', 'Calle 123 #45-67, Envigado', '6044444560');

-- (El password hash se generará en el Fase 5, por ahora ponemos un placeholder)
INSERT INTO Usuarios (nombre_completo, email, password_hash, rol, id_sede_asignada)
VALUES ('Super Admin', 'super@workhub.com', 'placeholder', 'SuperAdmin', NULL);

INSERT INTO Usuarios (nombre_completo, email, password_hash, rol, id_sede_asignada)
VALUES ('Admin Envigado', 'admin@workhub.com', 'placeholder', 'Admin', 1);

INSERT INTO Planes (nombre_plan, precio, beneficios, creditos_reserva_mes)
VALUES ('Hot Desk Flexible', 350000, 'Acceso 24/7, Café ilimitado', 5);