<?xml version="1.0"?>
<!--+
    | 
    | merges the doubled entries as a result of the source_lang-files inversion process 
    | Usage: java -Xmx2048m net.sf.saxon.Transform -it main THIS_SCRIPT inFile=INPUT_FILE.xml
    +-->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		xmlns:functx="http://www.functx.com"
		exclude-result-prefixes="xs functx">

  <xsl:strip-space elements="*"/>
  <xsl:output method="xml" name="xml"
              encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>

  <xsl:function name="functx:is-node-in-sequence-deep-equal" as="xs:boolean" 
		xmlns:functx="http://www.functx.com" >
    <xsl:param name="node" as="node()?"/> 
    <xsl:param name="seq" as="node()*"/> 
    
    <xsl:sequence select=" 
			  some $nodeInSeq in $seq satisfies deep-equal($nodeInSeq,$node)
			  "/>
    
  </xsl:function>
  
  <xsl:function name="functx:distinct-deep" as="node()*" 
		xmlns:functx="http://www.functx.com" >
    <xsl:param name="nodes" as="node()*"/> 
    
    <xsl:sequence select=" 
			  for $seq in (1 to count($nodes))
			  return $nodes[$seq][not(functx:is-node-in-sequence-deep-equal(
			  .,$nodes[position() &lt; $seq]))]
			  "/>
  </xsl:function>



  <xsl:function name="functx:substring-before-if-contains" as="xs:string?">
    <xsl:param name="arg" as="xs:string?"/> 
    <xsl:param name="delim" as="xs:string"/> 
    
    <xsl:sequence select=" 
			  if (contains($arg,$delim))
			  then substring-before($arg,$delim)
			  else $arg
			  "/>
  </xsl:function>
  
  <xsl:function name="functx:value-intersect" as="xs:anyAtomicType*">
    <xsl:param name="arg1" as="xs:anyAtomicType*"/> 
    <xsl:param name="arg2" as="xs:anyAtomicType*"/> 
    
    <xsl:sequence select=" 
			  distinct-values($arg1[.=$arg2])
			  "/>
  </xsl:function>

  <xsl:function name="functx:value-except" as="xs:anyAtomicType*">
    <xsl:param name="arg1" as="xs:anyAtomicType*"/> 
    <xsl:param name="arg2" as="xs:anyAtomicType*"/> 
    
    <xsl:sequence select=" 
			  distinct-values($arg1[not(.=$arg2)])
			  "/>
  </xsl:function>

  
  <!-- Input files -->
  <xsl:param name="inFile" select="'default.xml'"/>
  
  <!-- Output dir, files -->
  <xsl:variable name="outputDir" select="concat('to_filter_', $slang)"/>
  <xsl:param name="slang" select="'rus'"/>
  
  <!-- Patterns for the feature values -->
  <xsl:variable name="output_format" select="'xml'"/>
  <xsl:variable name="e" select="$output_format"/>
  <xsl:variable name="file_name" select="substring-before((tokenize($inFile, '/'))[last()], '.xml')"/>
  <xsl:variable name="debug" select="true()"/>
  <xsl:variable name="nl" select="'&#xa;'"/>
  
  <xsl:template match="/" name="main">
    <xsl:choose>
      <xsl:when test="doc-available($inFile)">
	<xsl:variable name="out_tmp">
	  <r>
	    <xsl:copy-of select="doc($inFile)/r/@*"/>
	    <xsl:attribute name="xml:lang">
	      <xsl:value-of select="$slang"/>
	    </xsl:attribute>
	    <xsl:for-each-group select="doc($inFile)/r/e" group-by="./lg/l">
	      
	      <xsl:variable name="c_lemma" select="current-grouping-key()"/>
	      
	      <xsl:variable name="t_variants">
		<all_t>
		  <xsl:for-each select="current-group()//mg/tg/t">
		    <t pos="{./@pos}">
		      
		      <xsl:if test="./@l_alt">
			<xsl:attribute name="l_alt">
			  <xsl:value-of select="normalize-space(./@l_alt)"/>
			</xsl:attribute>
		      </xsl:if>
		      
		      <xsl:attribute name="sem-cl">
			<xsl:for-each select="../../semantics/sem">
			  <xsl:value-of select="@class"/>
			  <xsl:if test="not(position() = last())">
			    <xsl:value-of select="'-'"/>
			  </xsl:if>
			</xsl:for-each>
		      </xsl:attribute>
		      
		      <xsl:attribute name="src">
			<xsl:for-each select="../../../sources/*">
			  <xsl:value-of select="@*"/>
			  <xsl:if test="not(position() = last())">
			    <xsl:value-of select="'-'"/>
			  </xsl:if>
			</xsl:for-each>
		      </xsl:attribute>
		      
		      <xsl:if test=".[not(@stat and @stat='pref')]/../..">
			<xsl:attribute name="rus-stat">
			  <xsl:value-of select="'yes'"/>
			</xsl:attribute>
		      </xsl:if>
		      
		      <xsl:value-of select="."/>
		    </t>
		  </xsl:for-each>
		</all_t>
	      </xsl:variable>

	      <xsl:if test="current-group()[@stat and @stat='pref']">
		<xsl:for-each select="current-group()[@stat and @stat='pref']">
		  <xsl:variable name="cID">
		    <xsl:if test="count(current-group()[@stat and @stat='pref']) = 1">
		      <xsl:value-of select="concat(./lg/l, '_', ./lg/l/@pos)"/>
		    </xsl:if>
		    <xsl:if test="count(current-group()[@stat and @stat='pref']) &gt; 1">
		      <xsl:value-of select="concat(position(), '_', ./lg/l, '_', ./lg/l/@pos)"/>
		    </xsl:if>
		  </xsl:variable>

		  <e id="{$cID}">
		    <xsl:copy-of select="./@*"/>
		    <xsl:copy-of select="./lg"/>
		    <xsl:copy-of select="./sources"/>
		    <mg>
		      <xsl:copy-of select="./mg/semantics"/>
		      <tg xml:lang="sjd">
			<xsl:variable name="curr_t" select="./mg/tg/t"/>
			<t pos="{./mg/tg/t/@pos}" stat="pref">

			  <xsl:if test="$curr_t/@l_alt">
			    <xsl:attribute name="l_alt">
			      <xsl:value-of select="normalize-space($curr_t/@l_alt)"/>
			    </xsl:attribute>
			  </xsl:if>
			  
			  <xsl:value-of select="$curr_t"/>
			</t>
			<xsl:copy-of select="$t_variants/all_t/t[not(. = $curr_t)]"/>
		      </tg>
		    </mg>
		  </e>
		</xsl:for-each>
	      </xsl:if>
	    </xsl:for-each-group>
	  </r>
	</xsl:variable>
	
	<!-- out -->
	<xsl:result-document href="{$outputDir}/{$file_name}.{$e}" format="{$output_format}">
	  <xsl:copy-of select="$out_tmp"/>
	</xsl:result-document>

      </xsl:when>
      <xsl:otherwise>
	<xsl:text>Cannot locate: </xsl:text><xsl:value-of select="$inFile"/><xsl:text>&#xa;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
</xsl:stylesheet>
