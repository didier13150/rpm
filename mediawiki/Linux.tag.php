<?php

$wgHooks['ParserFirstCallInit'][] = 'linuxParserInit';

// Hook our callback function into the parser
function linuxParserInit( Parser $parser ) {
        // When the parser sees the <sample> tag, it executes 
        // the wfSampleRender function (see below)
        $parser->setHook( 'path', 'pathRender' );
        $parser->setHook( 'package', 'packageRender' );
        $parser->setHook( 'app', 'appRender' );
        $parser->setHook( 'class', 'classRender' );
        $parser->setHook( 'previous', 'previousPage' );
        $parser->setHook( 'showterm', 'showtermRender' );
        // Always return true from this function. The return value does not denote
        // success or otherwise have meaning - it just must always be true.
        return true;
}

// Execute 
function pathRender( $input, array $args, Parser $parser, PPFrame $frame ) {
        // Nothing exciting here, just escape the user-provided
        // input and throw it back out again
        //$parser->disableCache();
        return '<span style="color:#6c06d1;font-weight:bold;font-style:italic;">' . htmlspecialchars( $input ) . '</span>';
}

function packageRender( $input, array $args, Parser $parser, PPFrame $frame ) {
        return '<span style="color:#9d4800;font-weight:bold;">' . htmlspecialchars( $input ) . '</span>';
}

function appRender( $input, array $args, Parser $parser, PPFrame $frame ) {
        return '<span style="color:#008080;font-weight:bold;">' . htmlspecialchars( $input ) . '</span>';
}

function classRender( $input, array $args, Parser $parser, PPFrame $frame ) {
        return '<span style="color:#0000aa;font-weight:bold;">' . htmlspecialchars( $input ) . '</span>';
}

function previousPage( $input, array $args, Parser $parser, PPFrame $frame ) {
        return '<a href="javascript:history.go(-1)">' . htmlspecialchars( $input ) . '</a>';
}

function showtermRender( $input, array $args, Parser $parser, PPFrame $frame ) {
        $width = 640;
        $height = 480;
        $border = 0;
        if ( isset( $args['width'] ) && intval( $args['width'] ) ) $width = intval( $args['width'] );
        if ( isset( $args['height'] ) && intval( $args['height'] ) ) $height = intval( $args['height'] );
        if ( isset( $args['border'] ) && intval( $args['border'] ) ) $border = intval( $args['border'] );
        return '<iframe src="https://showterm.b2pweb.com/' . htmlspecialchars( $input ) . '" width="' . $width . '" height="' . $height . '" border="' . $border . '"></iframe>';
}
