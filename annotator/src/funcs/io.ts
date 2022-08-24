export async function getInputFile(): Promise<any> {
  const pickerOpts = {
    types: [
      {
        description: "JSON file",
        accept: {
          "application/*": [".json"],
        },
        excludeAcceptAllOption: true,
        multiple: false,
      },
    ],
  };
  const [fileHandle] = await window.showOpenFilePicker(pickerOpts);
  const fileInfo = await fileHandle.getFile();
  return fileInfo;
}

export async function getOutputFile(): Promise<any> {
  const pickerOpts = {
    suggestedName: "annotation_results.json",
    types: [
      {
        description: "JSON file",
        accept: {
          "application/*": [".json"],
        },
      },
    ],
  };
  return await window.showSaveFilePicker(pickerOpts);
}
