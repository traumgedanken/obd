<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Cookers</title>
</head>
<body>
<table border="1">
  <tbody>
    <tr>
      <th>Image</th>
      <th>Name</th>
      <th>Price</th>
      <th>Description</th>
   </tr>
  <xsl:for-each select="//good">
    <tr>
      <td>
        <img src="{image}"/></td>
      <td><xsl:value-of select="@name"/></td>
      <td><xsl:value-of select="price"/> грн</td>
      <td><xsl:value-of select="description"/></td>
    </tr>
  </xsl:for-each>
</tbody>
</table>
</body>
</html>

</xsl:template>
</xsl:stylesheet>