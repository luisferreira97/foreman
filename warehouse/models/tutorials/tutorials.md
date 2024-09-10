{% docs tutorials %}

Table contains information about the hands-on tutorials.

Each tutorial is uniquely identified by the `id`. The `speaker_id` column is a foreign key for column `id` of the `speakers` table and references the tutor for the hands-on tutorial.

As opposed to the `sessions` this model does not track location and date information as all tutorials will be held on the 23rd of September at Porto Business School.

{% enddocs %}