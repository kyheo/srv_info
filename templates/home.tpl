<html>
<head>
    <title>SRV_INFO - Event log</title>
</head>
<body>
  <h1>Event log</h1>
  <h2>Filter</h2>
  <form method="post">
    <b>Client</b>
    <select name='client' id='client'>
      <option value="">-- Pick one (optional) --</option>
      {% for client in clients %}
      <option value="{{ client.key }}">{{ client.name }}</option>
      {% endfor %}
    </select>
    <b>Category</b>
    <select name='category' id='category'>
      <option value="">-- Pick one (optional) --</option>
      {% for category in categories %}
      <option value="{{ category.key }}">{{ category.name }}</option>
      {% endfor %}
    </select>
    <input type="submit" value="Filter">
  </form>
  <h2>Entries</h2>
  <table border="2" width="100%">
    <tr>
      <th>Datetime</th>
      <th>Client (ip)</th>
      <th>Category</th>
      <th>Data</th>
    </tr>
{% for event in events %}
    <tr style="background-color: {{ event.alert_color }};">
      <td align="center">{{ event.date }}</td>
      <td align="center"><b>{{ event.client.name }}</b> ({{ event.ip }})</td>
      <td align="center">{{ event.category.name }}</td>
      <td align="center">{{ event.short_detail }}</td>
    </tr>
{% endfor %}
  </table>
  <hr>
  <i>Page generated on {{ now }}</i>
</body>
</html>
