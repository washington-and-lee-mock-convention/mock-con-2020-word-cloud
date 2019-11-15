#!/usr/bin/env ruby

require "sequel"
DB = Sequel.connect ENV["DATABASE_URL"]
puts "Cleaning old sessions..."
DB["
    ALTER TABLE newsfeed ADD COLUMN hash text;
    DELETE FROM newsfeed
        WHERE url NOT IN (SELECT min(url)
                         FROM newsfeed
                         GROUP BY hash HAVING count(*) >= 1);
    ALTER TABLE newsfeed DROP COLUMN hash;
"]
puts "done."