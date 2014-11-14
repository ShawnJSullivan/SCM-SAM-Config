application-configurations test-repo for the config-blender service
==========================

This repo is being used for testing the config-blender app, and some of the config files have been converted to work
this app.

I worked on the configuration/USAT directory, and picked ios_iphone_2p5p3 as the final config.

For each of the names below, I created a sub-directory, copied *.json into prod.json in that directory:
<pre>
ios_iphone_2p5p3
ios_iphone_2
ios_iphone
ios
GDPIPUSCP
GDPIPUSCP_2
GDPSAM
GDP
</pre>

This matches the inheritance chain created from the SAM namespaces for ios_iphone_2p5p3.

Added these lines to top of ios_iphone_2p5p3/prod.json:
<pre>
    "@context": {"@vocab": "uri://GannettDigital.com/vocab#"},
    "@id": "scm_sam/USAT/ios_iphone_2p5p3/prod/release",
    "@parent_urls": ["scm_sam/USAT/GDP/prod/release",
                     "scm_sam/USAT/GDPSAM/prod/release",
                     "scm_sam/USAT/ios_iPhone_2/prod/release"],
</pre>

And similarly, for all the new */prod.json files. Staging would be similar, with stage.json under each new directory.

The second diagram on this page,shows the inheritance chain (if you pretend "markets" is "scm_sam"):
https://gannett.jira.com/wiki/display/GDPDW/Config+Service

