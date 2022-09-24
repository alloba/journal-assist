# Journal Assist 

This tool provides a simple way to quickly add onto and create new journal entries. 
It's really just a fancy way to say "open a file in neovim and automatically commit it to source tracking".

Written in python because I can pretty much guarantee that I will have it installed on every machine I touch. 

## Usage

On invocation, this tool will either open or create a file that is titled with the current date, in a designated journal directory. 
The journal directory is expected to be provided as part of the command.
The ultimate intention is that the command paired with the correct journal directory will be set by the user in their bash profile (or similar).

So, something like below: 

`journal-assist ~/notes/journal/`

If an appropriate file does not exist in the provided directory (a file titled with the current date), a new one will be created using the default template. 

Templates are stored in the 'templates' directory. 
The only one that exists is the default template, and the entire concept really only exists as a jumping off point for when I realize there is some other format I would like to use sometimes. 
*This also means that there is no way to use a different template even if it is created. That behavior would have to be implemented in the tool first.*


