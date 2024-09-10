{% docs sessions %}

Table contains information about the presentation sessions, including content details, time and location.

Each session is uniquely identified by the combination of `id` and `speaker_id`, as a session can have more than one presenter. The `speaker_id` column is a foreign key for column `id` of the `speakers` table.

The sessions are also divided by their `type`: short or long. Note that Hands-On Tutorials, while part of the same agenda, are kept in a separate model named `tutorials`.

{% enddocs %}