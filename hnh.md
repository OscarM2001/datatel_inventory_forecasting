erDiagram
    %% Tabla principal de productos
    ds_Product_Items {
        BIGINT ID_Producto PK
        VARCHAR Nombre_Producto
        INT Stock_Actual
        VARCHAR Categoria
        DECIMAL Precio_Unitario
        DATETIME aud_Fecha_Creacion
        DATETIME aud_Fecha_Modificacion
        NVARCHAR aud_Usuario_Creacion
        NVARCHAR aud_Usuario_Modificacion
        CHAR estado
    }

    %% Tabla de clientes
    ds_Clientes {
        BIGINT ID_Cliente PK
        NVARCHAR Nombre
        NVARCHAR Email UNIQUE
        NVARCHAR Telefono
        NVARCHAR Direccion
        DATETIME Fecha_Registro
        BIT Activo
        CHAR estado
        DATETIME aud_Fecha_Creacion
        DATETIME aud_Fecha_Modificacion
        NVARCHAR aud_Usuario_Creacion
        NVARCHAR aud_Usuario_Modificacion
    }

    %% Tabla de servicios contratados (cabecera)
    ds_Servicios_Contratados_Cab {
        BIGINT ID_Venta PK
        BIGINT ID_Servicio FK
        VARCHAR TipoServicio
        BIGINT ID_Cliente FK
        DATETIME Fecha_Venta
        DECIMAL Total_Venta
        CHAR estado
        DATETIME aud_Fecha_Creacion
        DATETIME aud_Fecha_Modificacion
        NVARCHAR aud_Usuario_Creacion
        NVARCHAR aud_Usuario_Modificacion
    }

    %% Tabla de servicios contratados (detalle)
    ds_Servicios_Contratados_Det {
        BIGINT ID_Detalle PK
        BIGINT ID_Venta FK
        BIGINT ID_Producto FK
        INT CantidadVendida
        DECIMAL Precio_Unitario
        DATETIME aud_Fecha_Creacion
        DATETIME aud_Fecha_Modificacion
        NVARCHAR aud_Usuario_Creacion
        NVARCHAR aud_Usuario_Modificacion
    }

    %% Tabla de catálogo de servicios
    ds_Catalogo_Servicios {
        BIGINT ID_Servicio PK
        VARCHAR Nombre_Servicio
        DATETIME aud_Fecha_Creacion
        NVARCHAR aud_Usuario_Creacion
    }

    %% Tabla de dataset analítico
    DATATEL_Ventas_Inventario_Analytical_Dataset {
        DATETIME Fecha_Venta
        BIGINT ID_Cliente FK
        BIGINT ID_Producto FK
        INT Cantidad_Vendida
        DECIMAL Precio_Unitario
        DECIMAL Total_Venta
        INT Stock_Actual
        VARCHAR CategoríaProducto
        DATETIME aud_Fecha_Creacion
        DATETIME aud_Fecha_Modificacion
        NVARCHAR aud_Usuario_Creacion
        NVARCHAR aud_Usuario_Modificacion
    }

    %% Relaciones entre tablas
    ds_Servicios_Contratados_Cab ||--o{ ds_Servicios_Contratados_Det : "contiene"
    ds_Servicios_Contratados_Cab }o--|| ds_Clientes : "pertenece a"
    ds_Servicios_Contratados_Cab }o--|| ds_Catalogo_Servicios : "relacionado con"
    ds_Servicios_Contratados_Det }o--|| ds_Product_Items : "incluye"
    DATATEL_Ventas_Inventario_Analytical_Dataset }o--|| ds_Clientes : "pertenece a"
    DATATEL_Ventas_Inventario_Analytical_Dataset }o--|| ds_Product_Items : "contiene"