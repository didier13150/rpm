<?php
 
# To activate the extension, include it from your LocalSettings.php
# with: include("extensions/calcBitrate.php");
# 
# Syntaxe: <CalcBitrate/>
#

 
$wgExtensionFunctions[] = "wfCalcBitrate";
 
function wfCalcBitrate() {
    global $wgParser;
 
    $wgParser->setHook( "CalcBitrate", "renderCalcBitrate" );
}
 
# The callback function for converting the input text to HTML output
function renderCalcBitrate() {
//    global $wgOut;
    # Parser
//    $input = $wgOut->parse($input,false);    
    $style = ' style="width:80px"';
    $output = '<!-- CalcBitrate -->';
    #please check the path to the javascript file and adjust it, if necessary
    $output .= '<script type="text/javascript" src="/wiki/extensions/CalcBitrate/CalcBitrate.js">';
    $output .= '</script>';
    $output .= '<div><center>';
    $output .= '<form name="bitrate";">';
    $output .= '<input type="hidden" name="ie" value="UTF-8"/>';
    $output .= '<input type="hidden" name="oe" value="UTF-8"/>';
    $output .= '<table style="background-color: #f9f6b7; border: 1px solid #c4c295; color: black; padding: 5px; margin: 1ex 0; min-height: 48px;"><tr>';
    $output .= '<th colspan="2">Calculateur de bitrate</th></tr><tr>';  
    $output .= '<td><label for="size">Taille de la video souhait&eacute;e en Mo</label></td>';
    $output .= '<td><input type="text" name="size" cols="10" value="0"'.$style.'/></td>';
    $output .= '</tr><tr>';
    $output .= '<td><label for="audio1">Tailles des pistes audio en Mo</label></td>';
    $output .= '<td><input type="text" name="audio1" cols="10" value="0"'.$style.'/>';
    $output .= '<input type="text" name="audio2" cols="10" value="0"'.$style.'/>';
    $output .= '<input type="text" name="audio3" cols="10" value="0"'.$style.'/>';
    $output .= '<input type="text" name="audio4" cols="10" value="0"'.$style.'/></td>';
    $output .= '</tr><tr>';
    $output .= '<td><label for="subtitle">Nombre de sous-titre</label></td>';
    $output .= '<td><input type="text" name="subtitle" cols="10" value="0"'.$style.'/></td>';
    $output .= '</tr><tr>';
    $output .= '<td><label>Dur&eacute;e de la vid&eacute;o:</label></td>';
    $output .= '<td><input type="text" name="hour" cols="10" value="0"'.$style.'/>';
    $output .= '<label for="hour">H</label>';
    $output .= '<input type="text" name="minute" cols="10" value="0"'.$style.'/>';
    $output .= '<label for="minute">M</label>';
    $output .= '<input type="text" name="seconde" cols="10" value="0"'.$style.'/>';
    $output .= '<label for="seconde">S</label></td>';
    $output .= '</tr><tr>';
    $output .= '<td><input style="font-weight:bold;" type="button" value="Calculer le bitrate" onclick="calculate()"/></td>';
    $output .= '<td><input type="text" name="answer" cols="10" value="0"'.$style.'/></td>';
    $output .= '</tr></table>';
    $output .= '</form></center></div>';
    $output .= '<script type="text/javascript">';
    $output .= 'calculate();';
    $output .= '</script>';
    $output .= '<!-- CalcBitrate -->';
    return $output;
}

