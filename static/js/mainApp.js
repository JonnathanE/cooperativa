document.addEventListener('DOMContentLoaded', function () {
    M.AutoInit();
});

$(document).ready(function () {
    $('#factura').hide();
    $('#ingresarProducto').hide();
    $('#buscarProducto').hide();
    $('#nuevoCliente').hide();

    // DESPLEGAR MENU LATERAL IZQUIERDO
    $('#show-menu').change(function () {
        if ($('.menu').width() == "140") {
            $('.menu').animate({ width: '-=80px' });
            $(".ocultar").hide();
            $(".menu i").show();
        } else {
            $(".menu").animate({ width: '+=80px' });
            $(".ocultar").show("slow");
        }
    });

    // MOSTRAR FACTURA
    $('#mostrar_factura').on('click', function () {
        $('#inicio').hide();
        $('#factura').show();
        $('#ingresarProducto').hide();
        $('#buscarProducto').hide();
        $('#nuevoCliente').hide();
    });

    // MOSTRAR EL INGRESO DE PRODUCTOS
    $('#mostrar_igrProducto').on('click', function () {
        $('#inicio').hide();
        $('#factura').hide();
        $('#ingresarProducto').show();
        $('#buscarProducto').hide();
        $('#nuevoCliente').hide();
    });

    // MOSTRAR BUSCAR PRODUCTOS
    $('#mostrar_bscProducto').on('click', function () {
        $('#inicio').hide();
        $('#factura').hide();
        $('#ingresarProducto').hide();
        $('#buscarProducto').show();
        $('#nuevoCliente').hide();
    });

    // MOSTRAR NUEVO CLIENTE
    $('#nuevo_cliente').on('click', function () {
        $('#inicio').hide();
        $('#factura').hide();
        $('#ingresarProducto').hide();
        $('#buscarProducto').hide();
        $('#nuevoCliente').show();
    });


    
    // MOSTRAR FACTURA MENU LATERAL IZQUIERDO
    $('#mostrar_factura_mi').on('click', function () {
        $('#inicio').hide();
        $('#factura').show();
        $('#ingresarProducto').hide();
        $('#buscarProducto').hide();
        $('#nuevoCliente').hide();
    });

    // MOSTRAR EL INGRESO DE PRODUCTOS MENU LATERAL IZQUIERDO
    $('#mostrar_igrProducto_mi').on('click', function () {
        $('#inicio').hide();
        $('#factura').hide();
        $('#ingresarProducto').show();
        $('#buscarProducto').hide();
        $('#nuevoCliente').hide();
    });

    // MOSTRAR BUSCAR PRODUCTOS MENU LATERAL IZQUIERDO
    $('#mostrar_bscProducto_mi').on('click', function () {
        $('#inicio').hide();
        $('#factura').hide();
        $('#ingresarProducto').hide();
        $('#buscarProducto').show();
        $('#nuevoCliente').hide();
    });

    // MOSTRAR NUEVO CLIENTE MENU LATERAL IZQUIERDO
    $('#nuevo_cliente_mi').on('click', function () {
        $('#inicio').hide();
        $('#factura').hide();
        $('#ingresarProducto').hide();
        $('#buscarProducto').hide();
        $('#nuevoCliente').show();
    });
});


