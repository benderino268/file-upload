#!-*- coding: utf-8 -*-
FORM = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<script src="//code.jquery.com/jquery-1.11.3.min.js"></script>
<script src="http://malsup.github.com/jquery.form.js"></script>
</head>
<body>
    <form id='form' action='' method='POST' enctype='multipart/form-data'>
        <span>Файл:</span>
        <input type='file' name='to_upload'/>
        <input type='button' onclick="$('#form').ajaxSubmit();" value='Загрузить'/>
    </form>
</body>
</html>
'''