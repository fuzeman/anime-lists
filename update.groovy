#!/usr/bin/env groovy

import java.util.zip.*
import javax.xml.transform.*
import javax.xml.transform.stream.*
import groovy.xml.*


def downloadGzipped = { out, url ->
    def file = new File(out)

    if(System.currentTimeMillis() - file.lastModified() < 24 * 60 * 60 * 1000) {
        println("Using existing animetitles (less than 24 hours old)")
        return
    }

	def stream = file.newOutputStream()

	def decoder = new GZIPInputStream(new URL(url).openStream())
	file << decoder
    decoder.close()

    stream.close()
}

def transform = { out, xs, xml -> 
    // Create transformer
    def transformer = TransformerFactory.newInstance()
    	.newTemplates(new StreamSource(xs as File))
    	.newTransformer()

    transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2")

    // Apply transformation
    def buffer = new StringWriter()

    transformer.transform(new StreamSource(xml as File), new StreamResult(buffer));

    // Write XML to file
    new File(out).withWriter('UTF-8') { writer ->
    	// Write XML declaration
    	writer.append('<?xml version="1.0" encoding="utf-8"?>\n')

	    // Write XML document
	    writer << buffer
	}
}

// Download titles from AniDB
downloadGzipped('.animetitles.xml', 'http://anidb.net/api/animetitles.xml.gz')

// Update titles
transform('anime-titles.xml', 'transforms/sort-animetitles.xsl', '.animetitles.xml')

// Update master
transform('anime-list-master.xml', 'transforms/update-anime-list-master.xsl', 'anime-titles.xml')

// Update children
transform('anime-list.xml', 'transforms/create-anime-list.xsl', 'anime-list-master.xml')
transform('anime-list-full.xml', 'transforms/create-anime-list-full.xsl', 'anime-list-master.xml')
transform('anime-list-unknown.xml', 'transforms/create-anime-list-unknown.xsl', 'anime-list-master.xml')
transform('anime-list-todo.xml', 'transforms/create-anime-list-todo.xsl', 'anime-list-master.xml')
transform('anime-movieset-list.xml', 'transforms/update-anime-movieset-list.xsl', 'anime-movieset-list.xml')
