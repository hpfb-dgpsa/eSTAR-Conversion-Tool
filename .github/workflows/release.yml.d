name: Create Release

on:
  workflow_run:
    workflows: ["Build Windows Executable"]
    types:
      - completed

permissions:
  contents: write

jobs:
  release:
    runs-on: windows-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    permissions:
      contents: write
      actions: read
      id-token: write
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: windows-executable

      - name: Create Release
        id: create_release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.event.workflow_run.head_branch }}
          release_name: Release ${{ github.event.workflow_run.head_branch }}
          draft: false
          prerelease: false

      - name: Verify Download
        run: ls -R ./dist
      - name: Verify release output 
        run: echo $steps.create_release.outputs.upload_url

      - name: Upload Release Asset
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./eSTAR_ConversionTool.exe
          asset_name: eSTAR_ConversionTool.exe 
          asset_content_type: application/vnd.microsoft.portable-executable
