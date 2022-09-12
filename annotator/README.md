# Ontology harmonization annotator (experimental)

This is the companion app for annotating phenotype mapping / harmonization results produced by the `phenotype mapper` app (unreleased).

Detailed documentation to this app is available under the "/docs" route (i.e. if the app is running locally at https://localhost:8080 then documentation is available at https://localhost:8080/docs).

This is a very early-stage release, so please keep regular backups of your files.

# Setting up

## Setting up in a local environment

To get a local instance of the app running, you must first ensure [npm is installed](https://nodejs.org/en/download/) and callable from the commandline.

After that, open a terminal and navigate to the directory containing this README file, then run the following commands

```sh
# this will install the dependency
npm install

# this will start the app, at https://localhost:8080
npm run serve
```

If all steps are finished successfully, you should be able to use the app in the browser from the URL https://localhost:8080.
To kill the app, simply stop the terminal session.
