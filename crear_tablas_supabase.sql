-- ==========================================================
-- SCRIPT DE CREACIÓN DE TABLAS — RECLAMOS ATC
-- Ejecutar en Supabase SQL Editor
-- ==========================================================

-- ==========================================================
-- TABLA: tickets
-- Consolidado principal — reemplaza CONSOLIDADO_ACTIVO.xlsx
-- ==========================================================
CREATE TABLE IF NOT EXISTS tickets (

    -- Identificador interno de Supabase
    id                  SERIAL PRIMARY KEY,

    -- Identificador único del negocio
    clave_unica         TEXT UNIQUE NOT NULL,

    -- ==============================================
    -- CAMPOS DEL EXCEL INPUT (vienen del sistema)
    -- ==============================================
    ticket              TEXT,
    usuario             TEXT,
    genero              TEXT,
    solicitud           TEXT,
    estado              TEXT,
    correo              TEXT,
    localidad           TEXT,
    distrito            TEXT,
    provincia           TEXT,
    departamento        TEXT,
    codigo_iib          TEXT,
    tipo_entidad        TEXT,
    n_documento_dni_ce  TEXT,

    -- Fechas del input
    fecha               TIMESTAMPTZ,
    fecha_averia        TIMESTAMPTZ,
    fecha_cierre_ticket TIMESTAMPTZ,

    -- ==============================================
    -- CAMPOS CALCULADOS POR PYTHON
    -- ==============================================
    senor_a             TEXT,
    identificado        TEXT,
    usuario_a           TEXT,
    resolucion          TEXT,
    paso_a_calidad      TEXT,
    cierre_ticket_reclamo_averia TEXT,

    -- Fechas calculadas
    fecha_inicia_reclamo_calidad        TIMESTAMPTZ,
    fecha_limite_resolucion             TIMESTAMPTZ,
    fecha_limite_cumplimiento           TIMESTAMPTZ,
    fecha_limite_elaboracion_carta      TIMESTAMPTZ,

    -- ==============================================
    -- CAMPOS MANUALES (solo el usuario los edita)
    -- ==============================================
    fecha_programada_mantenimiento_res  TIMESTAMPTZ,
    fecha_programada_mantenimiento_res2 TIMESTAMPTZ,
    n_ot                                TEXT,
    fecha_ot                            TIMESTAMPTZ,
    supervisor_mantenimiento            TEXT,
    colaborador_encargado               TEXT,
    declaracion_reclamo                 TEXT,
    quien_indico_fecha_atencion         TEXT,
    calidad_cerrado                     TEXT,
    fecha_resolucion                    TIMESTAMPTZ,
    fecha_notificacion_resolucion       TIMESTAMPTZ,
    medio_notificacion_reclamo          TEXT,
    motivo_no_cumplio_plazo             TEXT,
    descripcion_averia                  TEXT,
    fecha_cumplimiento                  TIMESTAMPTZ,
    aplica_carta_cumplimiento           TEXT,
    n_carta_cumplimiento                TEXT,
    fecha_elaboracion_carta             TIMESTAMPTZ,
    fecha_remision_carta                TIMESTAMPTZ,
    medio_notificacion_carta            TEXT,

    -- Timestamps de auditoría
    creado_en       TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en  TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para búsquedas frecuentes
CREATE INDEX IF NOT EXISTS idx_tickets_ticket       ON tickets(ticket);
CREATE INDEX IF NOT EXISTS idx_tickets_estado       ON tickets(estado);
CREATE INDEX IF NOT EXISTS idx_tickets_paso_calidad ON tickets(paso_a_calidad);
CREATE INDEX IF NOT EXISTS idx_tickets_fecha_averia ON tickets(fecha_averia);


-- ==========================================================
-- TABLA: historial
-- Registro de todos los cambios del sistema
-- ==========================================================
CREATE TABLE IF NOT EXISTS historial (
    id              SERIAL PRIMARY KEY,
    fecha_hora      TIMESTAMPTZ DEFAULT NOW(),
    usuario         TEXT,
    accion          TEXT,   -- TICKET NUEVO, ACTUALIZACION, EDICION, CARTA GENERADA, RESOLUCION GENERADA
    ticket          TEXT,
    clave_unica     TEXT,
    campo           TEXT,
    valor_anterior  TEXT,
    valor_nuevo     TEXT
);

CREATE INDEX IF NOT EXISTS idx_historial_ticket     ON historial(ticket);
CREATE INDEX IF NOT EXISTS idx_historial_usuario    ON historial(usuario);
CREATE INDEX IF NOT EXISTS idx_historial_fecha_hora ON historial(fecha_hora);
CREATE INDEX IF NOT EXISTS idx_historial_accion     ON historial(accion);


-- ==========================================================
-- TABLA: feriados
-- Días no laborables para cálculo de fechas
-- ==========================================================
CREATE TABLE IF NOT EXISTS feriados (
    id      SERIAL PRIMARY KEY,
    fecha   DATE UNIQUE NOT NULL
);


-- ==========================================================
-- TABLA: estado_sistema
-- Control de concurrencia — reemplaza estado.json
-- Solo tiene una fila con id=1
-- ==========================================================
CREATE TABLE IF NOT EXISTS estado_sistema (
    id      INTEGER PRIMARY KEY DEFAULT 1,
    estado  TEXT DEFAULT 'libre',
    usuario TEXT DEFAULT '',
    desde   TIMESTAMPTZ
);

-- Insertar la fila única de estado
INSERT INTO estado_sistema (id, estado, usuario)
VALUES (1, 'libre', '')
ON CONFLICT (id) DO NOTHING;


-- ==========================================================
-- FUNCIÓN: actualizar timestamp automáticamente
-- ==========================================================
CREATE OR REPLACE FUNCTION actualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_actualizar_tickets
    BEFORE UPDATE ON tickets
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();
