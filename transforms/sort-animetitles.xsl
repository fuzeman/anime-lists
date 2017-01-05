<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="xml" indent="yes" encoding="utf-8" omit-xml-declaration="yes" />
  <xsl:strip-space elements="*"/>

  <xsl:template match="comment()">
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:copy>
      <xsl:apply-templates select="@*" />
      <xsl:apply-templates />
    </xsl:copy>
    <xsl:text>&#xa;</xsl:text>
  </xsl:template>

  <xsl:template match="animetitles">
    <xsl:copy>
      <xsl:for-each select="anime">
        <anime>
          <xsl:attribute name="aid"><xsl:value-of select="@aid" /></xsl:attribute>
          <xsl:for-each select="title">
            <xsl:sort select="@type" />
            <xsl:sort select="@xml:lang" />
            <title>
            <xsl:attribute name="type"><xsl:value-of select="@type" /></xsl:attribute>
            <xsl:attribute name="xml:lang"><xsl:value-of select="@xml:lang" /></xsl:attribute>
            <xsl:value-of select="." /></title>  
          </xsl:for-each>
        </anime>
      </xsl:for-each>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>