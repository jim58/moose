#$Id: Webuser.pm,v 1.3 2010/03/28 19:05:23 jim Exp jim $
package Local::Webuser;

=head1	NAME

Local::Webuser - toolkit to manage Apache website user accounts

=head1 SYNOPSIS

  use Local::Webuser;

=head2	FUNCTIONS

	my $command = htpasswd('/usr/bin/htpasswd','/usr/apache2/bin/htpasswd');
	my @dbases  = list_dbases();
	my $code    = set_dbdir($path)
	my $xpass   = encrypt_pass($pass);

=head2	CLASS METHODS

	$p = Local::Webuser->new;
	$p = Local::Webuser->new($dbase)

=head2	INSTANCE METHODS

=head3	File Accessors

	($cnt, $msg) = $p->read_dbase($dbase)
	($cnt, $msg) = $p->write_dbase($dbase)
	($cnt, $msg) = $p->write_apache($dbase)


=head3	Database Accessors

	my @users   = $p->list_users();
	my @groups  = $p->list_groups();

	$p->addgroups('group1,group2');

	($xpass, $groups, $name, $email, $comment) = $p->get_record($user);
	$cnt = $p->put_record($user, $xpass, $groups, $name, $email, $comment);

	$my_xpass   = $p->xpass($user, $xpass);
	$my_groups  = $p->groups($user, $groups);
	$my_name    = $p->name($user, $name);
	$my_email   = $p->email($user, $email);
	$my_comment = $p->comment($user, $comment);


=head1 DESCRIPTION

This module consists of methods for managing web user accounts for Apache.

 An active user database consists of three files:
	default-records
	default-htpasswd
	default-htgroups



=head2 EXPORT

set_dbdir($path)

 set database directory to $path

list_dbases($path)

 returns a list of available databases


=cut


use 5.008008;
use strict;
use warnings;

require Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw( set_dbdir list_dbases );
our $VERSION = '0.01';


=head2	PACKAGE VARIABLES

=over 4

=item	$EXEC_HTPASSWD


=item	$DBDIR


=item	$ERR_CODE


=item	$ERR_MESSAGE


=back

=cut

#
# default search path
#
my @pathlist = (
	'/usr/bin/htpasswd',
	'/usr/apache2/bin/htpasswd',
	'/usr/local/bin/htpasswd',
);

our $EXEC_HTPASSWD = htpasswd(@pathlist)
	or die "can't find htpasswd binary";


our $DBDIR = '/opt/apache2/etc';


our $ERR_CODE = 0;

our $ERR_MESSAGE = '';



#------------------------------------------------------------------------------#

=head2	FUNCTIONS

=over 4

=item	set_dbdir($path)

 set the package variable $DBDIR

=cut

sub set_dbdir {
	my ($path) = @_;

	if (-d $path) {
		$DBDIR = $path;
		return($DBDIR);
	}

	return(undef);
}

#------------------------------------------------------------------------------#

=item	list_dbases($path)

defaults to listing databases in $DBDIR

	my @dbase = list_dbases();
	foreach my $dbase (@dbase) {
		$p = Local::Webuser->new($dbase)
		do_something($p);
	}



=cut

sub list_dbases {
	my ($path) = @_;
	my @dbases = ();
	my $dbdir  = $path || $DBDIR;
	opendir DIR, $dbdir or return(undef);
	my @files = sort grep /-records/, readdir DIR;
	closedir DIR;
	foreach (@files) {
		s/-records$//;
		push @dbases, $_;
	}
	return(@dbases);

}

#------------------------------------------------------------------------------#

=item	htpasswd

	find an executable file called htpasswd

	my @pathlist = ('/usr/bin/htpasswd', '/usr/apache2/bin/htpasswd');
	if (htpasswd(@pathlist)) {
		print "htpasswd executable found\n";
	}
	else {
		die "no htpasswd executable found";
	}
	my $command = $p->htpasswd(@pathlist);

=cut

sub htpasswd {
	if (@_) {
		foreach my $path (@_) {
			return($path) if (-x $path);
		}
	}
	return(undef);
}

#------------------------------------------------------------------------------#

=item	encrypt_pass

	encrypt the password

	my $xpass = encrypt_pass($pass);

=back

=cut

sub encrypt_pass {
	my ($pass) = @_;
	return(undef) unless ($pass);
	my $xpass = `$EXEC_HTPASSWD -nb nouser $pass`;
	$xpass =~ s/nouser://;
	chomp $xpass;
	chomp $xpass;
	return($xpass);

}

#------------------------------------------------------------------------------#
#
#
#	my $p = Local::Webuser->new();
#	$p->read_dbase('/var/www/etc/example');
#
#
#------------------------------------------------------------------------------#

=head2	CLASS METHODS


=over 4

=item	new

	$dbase = 'example';
	$p = Local::Webuser->new($dbase)

	will create/use files:
		/opt/apache2/etc/example-records
		/opt/apache2/etc/example-dir
		/opt/apache2/etc/example-pag

=back

=cut

sub new {
	my $this = shift;
	my ($dbase) = @_;
	my $class = ref($this) || $this;
	my $self = {};
	bless $self, $class;
	$self->read_dbase($dbase);
	return($self);
}

#------------------------------------------------------------------------------#

=head2	INSTANCE METHODS

=head3	File Accessors

=over 4

=item	read_dbase

	load datastructure from file $dbase

	($cnt, $msg) = $p->read_dbase($dbase)

	can be called on multiple files to merge user base
	later user entries will overwrite earlier ones

=cut

sub read_dbase {
	my ($self, $dbase) = @_;
	my $userfile = $DBDIR . '/' . $dbase . '-records';
	my $RECORD;
	my ($user, $xpass, $groups, $name, $email, $comment);
	my $cnt;

	if (-f $userfile) {
		if (open $RECORD, '<', $userfile) {
			while (<$RECORD>) {
				chomp;
				$cnt++;
				($user, $xpass, $groups, $name, $email, $comment)
					= split /:/;
				$self->xpass($user, $xpass);
				$self->groups($user, $groups);
				$self->name($user, $name);
				$self->email($user, $email);
				$self->comment($user, $comment);

				$self->addgroups($groups);
			}
			close $RECORD;
			return($cnt, 'ok');
		}
		else {
			return(0, "failed to open $userfile : $!");
		}
	}
	else {
		# new database
		return($cnt, 'ok');
	}
}




#------------------------------------------------------------------------------#

=item	write_dbase

	write datastructure to file $name

	($cnt, $msg) = $p->write_dbase($dbase)

=cut

sub write_dbase {
	my ($self, $dbase) = @_;
	my $userfile = $DBDIR . '/' . $dbase . '-records';
	my $RECORD;
	my ($user, $xpass, $groups, $name, $email, $comment);
	my $cnt;
	my $record;
	my @users;

	if (open $RECORD, '>', $userfile) {
		@users = $self->list_users();
		foreach $user ( @users ) {
			$cnt++;
			$xpass   = $self->xpass($user);
			$groups  = $self->groups($user);
			$name    = $self->name($user);
			$email   = $self->email($user);
			$comment = $self->comment($user);
			$record = join(':',
				$user, $xpass, $groups, $name, $email, $comment
			);
			print $RECORD $record, "\n";
		}
		close $RECORD;
		return($cnt, 'ok');
	}
	else {
		return(0, "failed to open $userfile : $!");
	}
}

#------------------------------------------------------------------------------#

=item	write_apache

	write datastructure to files for apache use

	($cnt, $msg) = $p->write_apache($dbase)

=back

=cut

sub write_apache {
	my ($self, $dbase) = @_;
	my $htpasswd = $DBDIR . '/' . $dbase . '-htpasswd';
	my $htgroups = $DBDIR . '/' . $dbase . '-htgroups';

	my $PASSWD;
	my $GROUPS;

	my ($user, $xpass, $groups, $name, $comment);
	my $cnt;
	my $record;
	my @users;
	my %group;
	my @htpasswd;

	@users = $self->list_users();

	open $PASSWD, '>', $htpasswd
		or return(0, "failed to open $htpasswd: $!");

	open $GROUPS, '>', $htgroups
		or return(0, "failed to open $htgroups: $!");


	foreach $user ( @users ) {
		$cnt++;
		$xpass   = $self->xpass($user);
		$groups  = $self->groups($user);

		#print         $user, ":", $xpass, "\n";
		print $PASSWD $user, ":", $xpass, "\n";

		if ($groups) {
			foreach my $group (split /,/, $groups) {
				$group{$group} .= " $user";
			}
		}

	}

	close $PASSWD;

	foreach my $group (sort keys %group) {
		if ($group) {
		print $GROUPS "$group:$group{$group}\n";
		}
		else {
			return(0, 'no groups');
		}
	}
	close $GROUPS;

	return($cnt, 'ok');
	
	

}

#------------------------------------------------------------------------------#

=head3	Database Accessors

=over 4

=item	list_users

	my @users = $p->list_users();

	records where $user begins with '_' are excluded

=cut

sub list_users {
	my ($self) = @_;
	my @users;
	foreach (sort keys %$self) {
		if (!/^_/) {
			push @users, $_;
		}
	}
	#my @users = sort keys %$self;
	#shift @users;
	return(@users);
}

#------------------------------------------------------------------------------#

=item	list_groups

	my @groups = $p->list_groups();

=cut

sub list_groups {
	my ($self) = @_;
	my @groups = ();
	my $groups = $self->groups('_groups');
	if ($groups) {
		@groups = split /,/, $groups;
	}

	return(@groups);
}

#------------------------------------------------------------------------------#
#

=item	get_record

	get values for $user

	($xpass, $groups, $name, $email, $comment) = $p->get_record($user);

=cut

sub get_record {
	my ($self, $user) = @_;
	return(undef) unless ($user);
	
	return(
		$self->xpass($user),
		$self->groups($user),
		$self->name($user),
		$self->email($user),
		$self->comment($user),
	)

}

#------------------------------------------------------------------------------#
#

=item	put_record
 
	put values into datastructure for $user

	$cnt = $p->put_record($user, $xpass, $groups, $name, $email, $comment);

	passing '-' or a null string for any of the parameters leaves that
	parameter unchanged

	returns a count of the changed fields

=cut

sub put_record {
	my ($self, $user, $xpass, $groups, $name, $email, $comment) = @_;
	return(undef) unless ($user);
	my $cnt = 0;
	
	if ($xpass eq '-')   { } # do not change
	elsif ($xpass)       { $self->xpass($user, $xpass); $cnt++; }
	else                 { } # do not change

	if ($groups eq '-')  { } # do not change
	elsif ($groups)      { $self->groups($user, $groups); $cnt++; }
	else                 { } # do not change

	if ($name eq '-')    { } # do not change
	elsif ($name)        { $self->name($user, $name); $cnt++; }
	else                 { } # do not change

	if ($email eq '-')   { } # do not change
	elsif ($email)       { $self->email($user, $email); $cnt++; }
	else                 { } # do not change

	if ($comment eq '-') { } # do not change
	elsif ($comment)     { $self->comment($user, $comment); $cnt++; }
	else                 { } # do not change

	return($cnt);
}

#------------------------------------------------------------------------------#

=item	xpass

	read/set the encrypted password

	$my_xpass = $p->xpass($user);
		read $xpass

	$my_xpass = $p->xpass($user, $xpass);
		set $xpass

=cut

sub xpass {
	my ($self, $user, $xpass) = @_;
	return(undef) unless ($user);
	return(undef) if ($user =~ /^_/);
	return(undef) if ($user eq '_groups');

	if ($xpass) {
		$self->{$user}{'XPASS'} = $xpass;
	}
	return ( $self->{$user}{'XPASS'} );
}

#------------------------------------------------------------------------------#

=item	addgroups

	add $groups to list of groups

	$cnt = $p->addgroups('group1,group2');
	print "There are ", $cnt, " groups now\n";

	returns the new total number of groups

=cut

sub addgroups {
	my ($self, $groups) = @_;
	my %group;	

	if ($self->{'_groups'}{'GROUPS'}) {
		$group{$_}++ foreach ( split /,/, $self->{'_groups'}{'GROUPS'} );
	}

	if ($groups) {
		$group{$_}++ foreach ( split /,/, $groups );
	}

	$self->{'_groups'}{'GROUPS'} = join(',', sort keys %group);

	return(scalar keys %group);
}


#------------------------------------------------------------------------------#

=item	groups

	read/set a comma separated list of groups

	$my_groups = $p->groups($user);
		read $groups

	$my_groups = $p->groups($user, $groups);
		set $groups

=cut

#
sub groups {
	my ($self, $user, $groups) = @_;
	return(undef) unless ($user);

	if ($groups) {
		return(undef) if ($user =~ /^_/);
		$self->{$user}{'GROUPS'} = $groups;
	}
	return ( $self->{$user}{'GROUPS'} );
}


#------------------------------------------------------------------------------#

=item	name

	read/set the proper name of $user

	$my_name = $p->name($user);
		read $name

	$my_name = $p->name($user, $name);
		set $name

=cut

sub name {
	my ($self, $user, $name) = @_;
	return(undef) unless ($user);

	if ($name) {
		$self->{$user}{'NAME'} = $name;
	}
	return ( $self->{$user}{'NAME'} );
}


#------------------------------------------------------------------------------#

=item	email

	read/set the email address for $user

	$my_email = $p->email($user);

	$my_email = $p->email($user, $email);

=cut

sub email {
	my ($self, $user, $email) = @_;
	return(undef) unless ($user);

	if ($email) {
		$self->{$user}{'EMAIL'} = $email;
	}
	return ( $self->{$user}{'EMAIL'} );
}

#------------------------------------------------------------------------------#

=item	comment

	read/set the comment for $user

	$my_comment = $p->comment($user);
		read $comment

	$my_comment = $p->comment($user, $comment);
		set $comment

=back

=cut

sub comment {
	my ($self, $user, $comment) = @_;
	return(undef) unless ($user);

	if ($comment) {
		$self->{$user}{'COMMENT'} = $comment;
	}
	return ( $self->{$user}{'COMMENT'} );
}

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#

=item	error

	($code, $message) = $p->error;

=cut

sub error {
	my ($self) = @_;
	return($ERR_CODE, $ERR_MESSAGE);
}

#==============================================================================#

#
#

__END__

=head1 SEE ALSO

htpasswd(1)


=head1 AUTHOR

Jim Harris, E<lt>ja_harris@rogers.comE<gt>

=head1 COPYRIGHT AND LICENSE

Copyright (C) 2010 by Jim Harris

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself, either Perl version 5.8.8 or,
at your option, any later version of Perl 5 you may have available.

=head1	REVISIONS

	$Revision: 1.3 $

	$Source: /opt/tools/lib/Local/Webuser.pm,v $


	$Log: Webuser.pm,v $
	Revision 1.3  2010/03/28 19:05:23  jim
	only split $groups if it is not empty

	Revision 1.2  2010/03/22 00:48:19  jim
	cleanup layout
	add documentation
	add functions and methods

	Revision 1.1  2010/03/20 19:58:48  jim
	Initial revision




=cut

__END__

my $p = Local::Webuser->new();

$p->database('/opt/apache2/etc/sample');

# $record = 'jharris:password:webmaster,admin,staff:Jim Harris:Site Admin

foreach $record (@records) {
	($user, $pass, $groups, $name, $comment) = split /:/;
	@groups = split /,/, $groups;

	if ($single( P{
		$p->insert($user, $pass, $groups, $name, $comment);
	}
	else {
		$p->pass($user, $pass);
		if ($gsingle) {
			$p->groups($user, $groups);
		}
		else {
			foreach $group (split /,/, $groups) {
				$p->addgroup($group);
			}
		}
		$p->name($user, $name);
		$p->comment($user, $comment);
	}


}


