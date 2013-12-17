<?php

if ( !defined( 'MEDIAWIKI' ) ) {
        die( 'This file is an extension to MediaWiki and thus not a valid entry point.' );
}

$wgExtensionCredits['parserhook'][] = array(
        'name' => 'No Title',
        'version' => '0.2.0',
        'author' => array(
                'Nx',
                '...'
                ),
        'description' => 'Provides a magic word that allows to hide the title heading of a page',
        'url' => 'https://www.mediawiki.org/wiki/Extension:NoTitle'
);
 
$wgHooks['LanguageGetMagic'][] = 'NoTitle::addMagicWordLanguage';
$wgHooks['ParserBeforeTidy'][] = 'NoTitle::checkForMagicWord';
 
class NoTitle {
 
  public static function addMagicWordLanguage( &$magicWords, $langCode ) {
    switch ($langCode) {
    default:
      $magicWords['notitle'] = array( 0, '__NOTITLE__' );
    }
    MagicWord::$mDoubleUnderscoreIDs[] = 'notitle';
    return true;
  }
 
  public static function checkForMagicWord( &$parser, &$text ) {
    if ( isset( $parser->mDoubleUnderscores['notitle'] ) ) {
      $parser->mOutput->addHeadItem( '<style type="text/css">.firstHeading, .subtitle, #siteSub, #contentSub, .pagetitle { display:none; }</style>' );
    }
    return true;
  }

}