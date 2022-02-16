setenv LANG "en_US.utf-8"
setenv PATH "${PATH}:${HOME}/bin"
setenv PATH "${PATH}:${HOME}/.cargo/bin"
setenv PATH "${PATH}:/usr/local/bin:/usr/games/bin:/usr/sbin:/usr/local/mysql/bin:/sbin:/usr/local/texlive/2014/bin/x86_64-darwin:."
setenv PATH "/opt/local/bin:/opt/local/sbin:$PATH"
setenv PATH "/usr/local/graphviz-2.14/bin:$PATH"
setenv PATH "$HOME/bin:$PATH"
setenv BLOCKSIZE 1024

if ( $OSTYPE == "linux" ) then
    setenv GOPATH "/vagrant/go"
    setenv PATH "/usr/local/go/bin:$GOPATH/bin:$PATH"
else 
    setenv GOPATH "/vagrant/go"
    setenv PATH "/usr/local/go/bin:$GOPATH/bin:$PATH"
endif


if ( ! $?prompt ) exit


set hostname=`/bin/hostname | sed "s/\..*//"`
setenv TTY `tty`
setenv EDITOR emacs
setenv PAGER 'less -i -M -e -c'
setenv DISP "${HOST}:0"
setenv PS ps4


# Add an architecture-specific directory to your path. This way you can
# put your own SPARCstation binaries in ~/bin/sun4, DECstation binaries in 
# ~/bin/mips, etc.  
set history=100 noclobber
umask 022

#bindkey "^[delete" delete-word
bindkey "^[h" backward-delete-word
bindkey "^[H" backward-delete-word
bindkey "\310" backward-delete-word
bindkey "\350" backward-delete-word
bindkey "^R" i-search-back
bindkey "^S" i-search-fwd

# Pete's local modifications


if ( $TERM == "network" ) then
	setenv TERM vt220
endif

limit coredumpsize 0
unset ignoreeof
unset noclobber

alias a alias

a topc 'top -o cpu'
a gitauto 'git commit -a -m auto'
a gpull 'git pull origin master'
a greset 'git reset --hard FETCH_HEAD'
a gush 'git commit -a -m auto; git push origin master'
a gushm 'git commit -a -m \!*; git push origin master'
a gitRestage 'git reset HEAD; git checkout -- .'

a lk "grep \!* [^,]*.{cc,md,c,go,pl,html,h,py,s,H,U,tex,java}"
a lki "grep -i \!* [^,]*.{cc,md,c,go,pl,html,h,py,s,H,U,tex,java}"
a lkw "grep -w \!* [^,]*.{cc,md,c,go,pl,html,h,py,s,H,U,tex,java}"
a k kill -9 
a ka killall -KILL
a l ls -CF
a ll "ls -alh \!*"
a llm "ls -alh \!* | m"
a lsd "ls -alhd \!*"
a m 'less -i -M -e -c'

set prompt_info = "%m:%~> "
if ($?RUBY_VERSION) then
  set prompt_info = "[$RUBY_VERSION] $prompt_info"
endif
set prompt = "$prompt_info"


a tem '/usr/bin/stty rows 51 cols 93 ; emacs19'
a e 'emacs -nw '

