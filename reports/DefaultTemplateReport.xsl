<?xml version = "1.0" encoding = "UTF-8"?>
<xsl:stylesheet version="1.0" xmlns = "http://www.w3.org/1999/xhtml" xmlns:xsl = "http://www.w3.org/1999/XSL/Transform">

    <xsl:output encoding = "UTF-8" method = "xml"
            doctype-public = "-//W3C//DTD XHTML 1.0 Strict//EN"
            doctype-system = "DTD/xhtml1-strict.dtd"
            indent = "yes" omit-xml-declaration = "yes"/>

    <xsl:template name = "br">
        <xsl:text disable-output-escaping = "yes">&lt;br/&gt;</xsl:text>
    </xsl:template>

    <xsl:template name = "hr">
        <xsl:text disable-output-escaping = "yes">&lt;hr/&gt;</xsl:text>
    </xsl:template>

	<!-- ATTRIBUTE SECTION -->
	
	<xsl:template name = "statsRow">
        <xsl:param name = "nodes"/>
        <xsl:variable name = "lowercase" select = "'abcdefghijklmnopqrstuvwxyz'" />
        <xsl:variable name = "uppercase" select = "'ABCDEFGHIJKLMNOPQRSTUVWXYZ'" />
        <tr>
            <xsl:for-each select = "$nodes">
                <xsl:choose>
                    <xsl:when test = "name() = 'HitPoints'">
                        <td>HP: &#160;</td>
                    </xsl:when>
                    <xsl:when test = "name() = 'Fatigue'">
                        <td>End: &#160;</td>
                    </xsl:when>
                    <xsl:when test = "name() = 'Power'">
                        <td>Pow: &#160;</td>
                    </xsl:when>
					<xsl:when test = "name() = 'ArmorFactor'">
                        <td>AF: &#160;</td>
                    </xsl:when>
                    <xsl:when test = "name() = 'PowerPool'">
                        <td>%PP: &#160;</td>
                    </xsl:when>
                    <xsl:otherwise>
                        <td><xsl:value-of select = "translate(substring(name(),1,3), $lowercase, $uppercase)"/>: &#160;</td>
                    </xsl:otherwise>
                </xsl:choose>
                <td align = "right">
                    <xsl:value-of select = "TotalBonus"/>
                    <xsl:if test = "name()='PowerPool'"><xsl:text>%</xsl:text></xsl:if>
                    <xsl:text>&#160;</xsl:text>
                </td>
                <td>
                    <xsl:text>/ </xsl:text>
                    <xsl:value-of select = "Base + CapBonus + MythicalCapBonus"/>
                    <xsl:if test = "name()='PowerPool'"><xsl:text>%</xsl:text></xsl:if>
                    <xsl:text>&#160;</xsl:text>
                </td>
                <td>
                    <xsl:if test = "TotalCapBonus &gt; 0 or TotalMythicalCapBonus &gt; 0">
                        <xsl:text>(+</xsl:text><xsl:value-of select = "TotalCapBonus + TotalMythicalCapBonus"/><xsl:text>)</xsl:text>
                    </xsl:if>
                    <xsl:text>&#160;</xsl:text>
                </td>
                <td width = "15">&#160;</td>
            </xsl:for-each>
        </tr>
    </xsl:template>

    <xsl:template match = "Attributes">
		<xsl:call-template name = "br"/>
        <b>Attributes:</b>
        <xsl:call-template name = "hr"/>
        <table cellspacing = "0" cellpadding = "0">
            <xsl:call-template name = "statsRow">
                <xsl:with-param name = "nodes" select = "Strength|Intelligence|HitPoints|ArmorFactor"/>
            </xsl:call-template>
            <xsl:call-template name = "statsRow">
                <xsl:with-param name = "nodes" select = "Constitution|Piety|Fatigue"/>
            </xsl:call-template>
            <xsl:call-template name = "statsRow">
                <xsl:with-param name = "nodes" select = "Dexterity|Empathy|Power"/>
            </xsl:call-template>
            <xsl:call-template name = "statsRow">
                <xsl:with-param name = "nodes" select = "Quickness|Charisma|PowerPool"/>
            </xsl:call-template>
        </table>
        <xsl:call-template name = "br"/>
    </xsl:template>
	
	<!-- RESISTANCE SECTION -->
	
	<xsl:template name = "resistsRow">
        <xsl:param name = "nodes"/>
        <tr>
            <xsl:for-each select = "$nodes">
                <td><xsl:value-of select = "name()"/>: &#160;</td>
                <td align="right">
                    <xsl:value-of select = "TotalBonus"/>
                    <xsl:text>&#160;</xsl:text>
                </td>
                <td>
                    <xsl:text>/ </xsl:text>
                    <xsl:value-of select = "Base + MythicalCapBonus"/>
                    <xsl:text>&#160;</xsl:text>
                </td>
                <td>
                    <xsl:for-each select = "RacialBonus">
                        <xsl:text>(+</xsl:text><xsl:value-of select = "."/><xsl:text>)</xsl:text>
                    </xsl:for-each>
                    <xsl:text>&#160;</xsl:text>
                </td>
                <td width = "15">&#160;</td>
            </xsl:for-each>
        </tr>
    </xsl:template>

    <xsl:template match = "Resistances">
		<xsl:call-template name = "br"/>
        <b>Resistances:</b>
        <xsl:call-template name = "hr"/>
        <table cellspacing = "0" cellpadding = "0">
            <xsl:call-template name = "resistsRow">
                <xsl:with-param name = "nodes" select = "Crush|Body|Energy"/>
            </xsl:call-template>
            <xsl:call-template name = "resistsRow">
                <xsl:with-param name = "nodes" select = "Slash|Cold|Matter"/>
            </xsl:call-template>
            <xsl:call-template name = "resistsRow">
                <xsl:with-param name = "nodes" select = "Thrust|Heat|Spirit"/>
            </xsl:call-template>
            <xsl:call-template name = "resistsRow">
                <xsl:with-param name = "nodes" select = "Essence"/>
            </xsl:call-template>
        </table>
        <xsl:call-template name = "br"/>
    </xsl:template>
	
	<!-- BONUS SECTIONS (Skills, ToA Bonuse, PvE Bonuse, Mythical Bonus) -->
	
	<xsl:template name = "bonuslist">
        <xsl:param name = "title"/>
        <xsl:param name = "nodes"/>
		<xsl:call-template name = "br"/>
        <b><xsl:value-of select="$title"/>:</b>
        <xsl:call-template name = "hr"/>
        <table cellspacing = "0" cellpadding = "0">
            <xsl:for-each select = "$nodes">
                <tr>
                    <td align="right"><xsl:value-of select = "TotalBonus"/>&#160;</td>
                    <td>/ <xsl:value-of select = "Base"/>&#160;</td>
                    <xsl:choose>
                        <xsl:when test="@Text != ''">
                            <td><xsl:value-of select = "@Text"/></td>
                        </xsl:when>
                        <xsl:otherwise>
                            <td><xsl:value-of select = "name()"/></td>
                        </xsl:otherwise>
                    </xsl:choose>
                </tr>
            </xsl:for-each>
        </table>
        <xsl:call-template name = "br"/>
    </xsl:template>
	
	<!-- SLOT & ITEM SECTION -->

    <xsl:template match = "Slot">
        <xsl:variable name = "SlotNumber"><xsl:value-of select = "number(@Number) + 1"/></xsl:variable>
        <xsl:if test = "Type != 'Unused'">
            <xsl:choose>
                <xsl:when test = "@Type = 'Crafted'">
                    <tr>
                        <td><b> > </b><i> Gem <xsl:copy-of select = "$SlotNumber"/>:&#160;</i></td>
                        <td align = "center"><xsl:value-of select = "Amount"/>&#160;</td>
						<td>
							<xsl:choose>
								<xsl:when test = "Type = 'Skill' and substring(Effect, 1, 4) != 'All '">
									<xsl:value-of select = "Effect"/><xsl:text>&#160;</xsl:text>
									<xsl:value-of select = "Type"/>
								</xsl:when>
								<xsl:when test = "Type = 'Resistance'">
									<xsl:value-of select = "Effect"/><xsl:text>&#160;</xsl:text>
									<xsl:text>Resist</xsl:text>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select = "Effect"/>
								</xsl:otherwise>
							</xsl:choose>
                            <xsl:text> - </xsl:text><xsl:value-of select = "GemName"/>
                        </td>
                    </tr>
                </xsl:when>
                <xsl:otherwise>
                    <tr>
                        <td><b> > </b><i> Slot <xsl:copy-of select = "$SlotNumber"/>:&#160;</i></td>
                        <td align = "center"><xsl:value-of select = "Amount"/>&#160;</td>
                        <td>
							<xsl:choose>
								<xsl:when test = "Type = 'Skill' and substring(Effect, 1, 4) != 'All '">
									<xsl:value-of select = "Effect"/><xsl:text>&#160;</xsl:text>
									<xsl:value-of select = "Type"/>
								</xsl:when>
								<xsl:when test = "Type = 'Attribute Cap' and Effect != 'Hit Points' and Effect != 'Power' and Effect != 'Fatigue'">
									<xsl:value-of select = "Effect"/><xsl:text>&#160;</xsl:text>
									<xsl:value-of select = "Type"/>
								</xsl:when>
								<xsl:when test = "Type = 'Attribute Cap'">
									<xsl:value-of select = "Effect"/><xsl:text>&#160;</xsl:text>
									<xsl:text>Cap</xsl:text>
								</xsl:when>
								<xsl:when test = "Type = 'Resistance'">
									<xsl:value-of select = "Effect"/><xsl:text>&#160;</xsl:text>
									<xsl:text>Resist</xsl:text>
								</xsl:when>
								<xsl:when test = "Type = 'PvE Bonus'">
									<xsl:value-of select = "Effect"/><xsl:text>&#160;</xsl:text>
									<xsl:text>(PvE)</xsl:text>
								</xsl:when>
								<xsl:when test = "Type = 'Mythical Stat Cap' or Type = 'Mythical Resist Cap'">
									<xsl:value-of select = "Type"/><xsl:text>&#160;</xsl:text>
									<xsl:text>(</xsl:text><xsl:value-of select = "Effect"/><xsl:text>)</xsl:text>
								</xsl:when>
								<xsl:when test = "Type = 'Mythical Stat &amp; Cap' or Type = 'Mythical Resist &amp; Cap'">
									<xsl:value-of select = "Type"/><xsl:text>&#160;</xsl:text>
									<xsl:text>(</xsl:text><xsl:value-of select = "Effect"/><xsl:text>)</xsl:text>
								</xsl:when>
								<xsl:when test = "Type = 'Mythical Bonus'">
									<xsl:text>Mythical</xsl:text><xsl:text>&#160;</xsl:text>
									<xsl:value-of select = "Effect"/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select = "Effect"/>
								</xsl:otherwise>
							</xsl:choose>
                            <xsl:if test = "GemName != ''">
                                <xsl:text> - </xsl:text><xsl:value-of select = "GemName"/>
                            </xsl:if>
                        </td>
                    </tr>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template>

    <xsl:template match = "Item">
        <xsl:if test = "count(Slot) &gt; 0 and Equipped = 'True' ">
            <dl>
                <dt><b><xsl:value-of select = "Location" /></b></dt>
                <dt><i><xsl:value-of select = "Name"/></i></dt>
                <dt>
					<xsl:choose>
                        <xsl:when test = "Level != '' and Level != '0' and Level != '-1' ">
                            <xsl:text>Level: </xsl:text><xsl:value-of select = "Level"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>Level: N/A</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
					<xsl:if test = "Quality != '' and Quality != '0' and Quality != '-1' ">
						<xsl:text>,&#160; Quality: </xsl:text><xsl:value-of select = "Quality"/>
					</xsl:if>
                    <xsl:if test = "AFDPS != '' and AFDPS != '0' and AFDPS != '-1' ">
                        <xsl:text>,&#160; AF/DPS: </xsl:text><xsl:value-of select = "AFDPS"/>
                    </xsl:if>
                    <xsl:if test = "Speed != '' and Speed != '0' and Speed != '-1' ">
                        <xsl:text>,&#160; Speed: </xsl:text><xsl:value-of select = "Speed"/>
                    </xsl:if>
                    <xsl:if test = "Bonus != '' and Bonus != '0' and Bonus != '-1' ">
                        <xsl:text>,&#160; Bonus: </xsl:text><xsl:value-of select = "Bonus"/>
                    </xsl:if>
                </dt>
                <xsl:if test = "State = 'Crafted' or State = 'Legendary' ">
                    <dt>
                        <xsl:text>Imbue Points: </xsl:text>
						<xsl:value-of select = "Imbue"/><xsl:text> of </xsl:text><xsl:value-of select = "ImbueMax"/>
						<xsl:text>,&#160; Overcharge: </xsl:text>
						<xsl:value-of select = "Imbue - ImbueMax"/><xsl:text> (</xsl:text><xsl:value-of select = "Success"/><xsl:text>%)</xsl:text>
                    </dt>
                </xsl:if>
                <dt>
                    <table cellspacing = "0" cellpadding = "0">
                        <xsl:apply-templates select = "Slot"/>
                    </table>
                </dt>
                <dt>
                    <xsl:text>Utility: </xsl:text><xsl:value-of select = "Utility"/>
                </dt>
            </dl>
        </xsl:if>
    </xsl:template>
	
	<!-- DOCUMENT SECTION -->

    <xsl:template match = "/Template">
        <html>
            <head>
                <title>Template Report</title>
            </head>
            <body>
                <center><b>Template Report</b></center>
				<xsl:call-template name = "br"/>
                <xsl:apply-templates select = "Attributes"/>
                <xsl:apply-templates select = "Resistances"/>
                <xsl:for-each select = "Skills|Focus|TOABonuses|PVEBonuses|MythicalBonuses">
                    <xsl:if test = "count(./*) &gt; 0">
                        <xsl:choose>
                            <xsl:when test = "@Text != ''">
                                <xsl:call-template name = "bonuslist">
                                    <xsl:with-param name = "title" select = "@Text"/>
                                    <xsl:with-param name = "nodes" select = "./*"/>
                                </xsl:call-template>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:call-template name = "bonuslist">
                                    <xsl:with-param name = "title" select = "name()"/>
                                    <xsl:with-param name = "nodes" select = "./*"/>
                                </xsl:call-template>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:if>
                </xsl:for-each>
				<xsl:call-template name = "br"/>
                <b>Item Listing:</b>
                <xsl:call-template name = "hr"/>
                <xsl:apply-templates select = "Item"/>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
