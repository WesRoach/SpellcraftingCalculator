<?xml version = "1.0" encoding = "UTF-8"?>
<xsl:stylesheet version="1.0" xmlns = "http://www.w3.org/1999/xhtml" xmlns:xsl = "http://www.w3.org/1999/XSL/Transform">

    <xsl:output encoding = "UTF-8" method = "xml"
            doctype-public = "-//W3C//DTD XHTML 1.0 Strict//EN"
            doctype-system = "DTD/xhtml1-strict.dtd"
            indent = "yes" omit-xml-declaration = "yes"/>

    <xsl:template name = "br">
        <xsl:text disable-output-escaping="yes">&lt;br/&gt;</xsl:text>
    </xsl:template>
	
    <xsl:template name = "hr">
        <xsl:text disable-output-escaping="yes">&lt;hr/&gt;</xsl:text>
    </xsl:template>
	
	<xsl:template name = "brbr">
		<xsl:text disable-output-escaping = "yes">&lt;br/&gt;&lt;br/&gt;</xsl:text>
	</xsl:template>
	
	<xsl:template name = "indent">
		<xsl:text disable-output-escaping = "yes">&#160;&#160;&#160;&#160;</xsl:text>
	</xsl:template>

	<!-- ITEM SECTION -->

    <xsl:template match = "Items">
        <center><b>Locations</b></center>
        <xsl:call-template name = "hr"/>
		<xsl:for-each select = "Item">
			<b><xsl:call-template name = "indent"/><xsl:value-of select = "@Location"/></b>
			<ul>
			<xsl:for-each select = "Jewel">
				<li><xsl:value-of select = "."/></li>
			</xsl:for-each>
			</ul>
		</xsl:for-each>
		<xsl:call-template name = "br"/>
    </xsl:template>
	
	<!-- MATERIALS SECTION -->
	
	<xsl:template name = "Materials">
		<center><b>Materials</b></center>
		<xsl:call-template name = "hr"/>
		<xsl:for-each select = "Gems|Dusts|Liquids">
			<b><xsl:call-template name = "indent"/><xsl:value-of select = "name()"/>:</b>
			<ul>
			<xsl:for-each select = "Material">
				<li><xsl:value-of select = "@Amount"/>&#160;<xsl:value-of select = "@Material"/></li>
			</xsl:for-each>
			</ul>
		</xsl:for-each>
	</xsl:template>
	
	<!-- DOCUMENT SECTION -->

    <xsl:template match = "/Materials">
        <html>
            <head>
                <title>Materials Report</title>
            </head>
            <body>
				<xsl:apply-templates select = "Items"/>
				<xsl:call-template name = "Materials"/>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
