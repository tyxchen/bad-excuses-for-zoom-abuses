#!/usr/bin/env ruby

require 'nokogiri'

root = File.open('Monster Manual Bestiary.xml') { |f| Nokogiri::XML(f) }
monsters = root.css('monster').map{|m| m > 'name'}

#puts monsters

f = File.new('dnd-monsters.txt', 'w')
f.write(monsters.join("\n"))
f.close
