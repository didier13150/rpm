<?php

$wgHooks['ParserFirstCallInit'][] = 'linuxParserInit';

// Hook our callback function into the parser
function linuxParserInit( Parser $parser ) {
        // When the parser sees the <sample> tag, it executes 
        // the wfSampleRender function (see below)
        $parser->setHook( 'path', 'pathRender' );
        $parser->setHook( 'package', 'packageRender' );
        $parser->setHook( 'app', 'appRender' );
        $parser->setHook( 'class', 'myClassRender' );
        $parser->setHook( 'previous', 'myPreviousPage' );
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

function myClassRender( $input, array $args, Parser $parser, PPFrame $frame ) {
        return '<span style="color:#0000aa;font-weight:bold;">' . htmlspecialchars( $input ) . '</span>';
}

function myPreviousPage( $input, array $args, Parser $parser, PPFrame $frame ) {
        return '<a href="javascript:history.go(-1)">' . htmlspecialchars( $input ) . '</a>';
}


