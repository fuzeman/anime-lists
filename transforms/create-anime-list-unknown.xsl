<xsl:stylesheet
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:output method="xml" indent="yes" encoding="utf-8" omit-xml-declaration="yes" />
  <xsl:strip-space elements="*"/>

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="@*" />
      <xsl:apply-templates />
    </xsl:copy>
  </xsl:template>
 
  <xsl:template match='anime' />
 
  <xsl:template match='anime[@tvdbid = "unknown"]'> 
    <xsl:copy>
      <xsl:copy-of select='@*[. != ""]' />
      <xsl:apply-templates />
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>