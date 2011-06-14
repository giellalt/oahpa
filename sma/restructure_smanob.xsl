<?xml version="1.0"?>
<!--+
    | Usage: java -Xmx2048m net.sf.saxon.Transform -it main THIS_FILE inDir=DIR
    | 
    +-->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		xmlns:xhtml="http://www.w3.org/1999/xhtml"
		exclude-result-prefixes="xs">

<!--   <xsl:strip-space elements="*"/> -->
  <xsl:output method="xml" name="xml"
	      encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>
  
  <xsl:param name="inDir" select="'src'"/>
  <xsl:param name="slang" select="'sma'"/>
  <xsl:param name="tlang" select="'nob'"/>
  <xsl:variable name="outDir" select="'interim_restruct'"/>
  <xsl:variable name="of" select="'xml'"/>
  <xsl:variable name="e" select="$of"/>
  <xsl:variable name="debug" select="true()"/>
  <xsl:variable name="nl" select="'&#xa;'"/>

  <xsl:template match="/" name="main">
    <xsl:for-each select="for $f in collection(concat($inDir,'?recurse=no;select=*.xml;on-error=warning')) return $f">
      
      <xsl:variable name="current_file" select="(tokenize(document-uri(.), '/'))[last()]"/>
      <xsl:variable name="current_dir" select="substring-before(document-uri(.), $current_file)"/>
      <xsl:variable name="current_location" select="concat($inDir, substring-after($current_dir, $inDir))"/>
      
      <xsl:if test="$debug">
	<xsl:message terminate="no">
	  <xsl:value-of select="concat('-----------------------------------------', $nl)"/>
	  <xsl:value-of select="concat('processing file ', $current_file, $nl)"/>
	  <xsl:value-of select="'-----------------------------------------'"/>
	</xsl:message>
      </xsl:if>

      <xsl:variable name="c_file">
	<xsl:for-each select="./r">
	  <r>
	    <xsl:copy-of select="./@*"/>
	    <xsl:for-each select="./e">
	      <e>
		<xsl:copy-of select="./@*"/>
		<xsl:if test="not($debug)">
		  <xsl:call-template name="flatten_node">
		    <xsl:with-param name="theNode" select="."/>
		  </xsl:call-template>
		</xsl:if>
		<xsl:copy-of select="./lg"/>
		<xsl:copy-of select="./stem"/>
		<xsl:copy-of select="./apps"/>
		<xsl:for-each select="./mg">
		  <xsl:if test="not(./@xml:lang = 'sme')">
		    <!-- if there is only one tg in the mg just restructure it -->
		    <xsl:if test="count(./tg) = 1">
		      <gogo_1-tg>
			<mg>
			  <xsl:copy-of select="./@*"/>
			  <!-- semantics on the mg level -->
			  <xsl:if test="./tg/semantics">
			    <xsl:copy-of select="./tg/semantics"/>
			  </xsl:if>
			  <!-- if there is some t or re elements in
			       the tg just copy them without lang
			       flag; this goes to the tg element -->
			  <xsl:if test="./tg/*[starts-with(local-name(), 't') or starts-with(local-name(), 'r')]">
			    <tg xml:lang="{./tg/t[1]/@xml:lang}">
			      <xsl:copy-of select="./tg/@*"/>
			      <xsl:for-each select="./tg/*[starts-with(local-name(), 't') or starts-with(local-name(), 'r')]">
				<xsl:element name="{./local-name()}">
				  <xsl:copy-of select="./@pos"/>
				  <xsl:copy-of select="./@stat"/>
				  <xsl:copy-of select="./@tcomm"/>
				  <xsl:value-of select="."/>
				</xsl:element>
			      </xsl:for-each>
			    </tg>
			    <!-- otherwise don't copy empty
			         tg-elements as in the name.xml file:
			         optimization (unless otherwise
			         explicitly required by the sma-oahpa
			         group) -->
			  </xsl:if>
			</mg>
		      </gogo_1-tg>
		    </xsl:if>

		    <!-- if there are more tg-elements in a mg: check
		         the pair nob-swe -->
		    <xsl:if test="count(./tg) &gt; 1">
		      <gogo_more-tg>
			<xsl:copy-of select="."/>
		      </gogo_more-tg>
		    </xsl:if>
		    
		  </xsl:if>
		  <xsl:if test="./@xml:lang = 'sme'">
		    <gogo_sme>
		      <xsl:copy-of select="."/>
		    </gogo_sme>
		  </xsl:if>
		</xsl:for-each>
	      </e>
	    </xsl:for-each>
	  </r>
	</xsl:for-each>
      </xsl:variable>
      
      <xsl:if test="$debug">      
	<xsl:result-document href="{$outDir}/{$current_file}" format="{$of}">
	  <xsl:copy-of select="$c_file"/>
	</xsl:result-document>
      </xsl:if>
    </xsl:for-each>
    
  </xsl:template>
  
  <xsl:template name="flatten_node">
    <xsl:param name="theNode"/>
    
    <xsl:variable name="pattern">
      <xsl:for-each select="$theNode/*[not(./@xml:lang = 'sme')]">
	<xsl:value-of select="lower-case(local-name(.))"/>

	<xsl:if test="./@xml:lang and not(./@xml:lang = '')">
	  <xsl:value-of select="concat('-', ./@xml:lang)"/>
	</xsl:if>
	
	<xsl:if test="not(position() = last())">
	  <xsl:value-of select="'_'"/>
	</xsl:if>
      </xsl:for-each>
    </xsl:variable>
    
    <xsl:element name="{concat(lower-case(local-name($theNode)), '_test')}">
      <xsl:attribute name="stamp">
	<xsl:value-of select="$pattern"/>
      </xsl:attribute>
    </xsl:element>
  </xsl:template>



</xsl:stylesheet>
