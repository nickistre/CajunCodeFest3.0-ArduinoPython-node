<?php

if (isset($_REQUEST['messages'])) {
  $messages = $_REQUEST['messages'];
  $messages_decoded = json_decode($messages);
  file_put_contents('data.txt', var_export($messages_decoded, true));
}
else {
  file_put_contents('data.txt', var_export($_REQUEST, true));
}