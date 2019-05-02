#!C:/perl64/bin/perl -wT
use strict;
use CGI qw(:standard);
use HTML::Entities;
use DBI;
use JSON;

my $q = CGI->new;
my $table = 'appointments';
my @months = (
    'Jan','Feb','Mar','Apr',
    'May','Jun','Jul','Aug','Sep',
    'Oct','Nov','Dec'
);

if($q->param('ajax')){
	db_handler($q); #ajax call to retrieve data from DB
}elsif($q->param('submitForm') ){
	my $result = db_handler($q);
	print $q->redirect('/index.cgi'); #redirecting to same page to avoid resubmission on page load
}else{
	show_table(); #render HTML table, if no CGI params passed
}

sub connect_to_db {
	my $db_file = shift;
	my $dbh = DBI->connect("dbi:SQLite:dbname=$db_file","","",{AutoCommit=>0,RaiseError=>1,PrintError=>0})or die "Can't connect to database: $DBI::errstr"; 
	return $dbh;
}

sub create_table {
    my $dbh = shift;
    my $query = "CREATE TABLE IF NOT EXISTS $table (datetime  DATETIME NOT NULL, description TEXT)";
    $dbh->do($query) or die "Cannot create table : $!";
}

sub fetch_data {
    my $dbh = shift;
    my $search_string = shift;
    my $json_data = [];
    my $query = "SELECT * FROM $table";
    if($search_string){
        $query .= " WHERE description LIKE '%".$search_string."%'";
    }
	eval{
		my $stmt = $dbh->prepare($query);
		my $result = $stmt->execute();
		while(my $array_ref = $stmt->fetchrow_arrayref()){
			my ($date,$time) = parse_date($array_ref->[0]);
			my $row = {};
			$row->{date} = date_format($date);
			$row->{time} = time_format($time,0);
			$row->{desc} = $array_ref->[1];
			push @$json_data, $row;
		}
	};
	if($@){
		return "Failed";
	}
    return $json_data;
}

sub insert_data {
    my($dbh,$date,$time,$desc) = @_;
	$time = time_format($time,1);
	$desc = encode_entities($desc);
    my $date_time = $date." ".$time;
    my $query = "INSERT INTO $table (datetime,description) VALUES (?,?)";
    my $stmt = $dbh->prepare($query);
    my $result = $stmt->execute($date_time,$desc);
    $stmt->finish();
    if($@){
        $dbh->rollback();
		warn "Database error: $DBI::errstr\n";
		return "Wrong entry value. Please try again.";
    }else{
        $dbh->commit();
		return "Appointment has been successfully scheduled.";
    }
}

sub db_handler {
    my $params  = shift;
    my $json_data;
	my $dbh = connect_to_db("Appointments.db");
	create_table($dbh);
	if($params->param('submitForm')){ 
		my $result = insert_data($dbh,$params->param('date'),$params->param('time'),$params->param('desc'));
		$dbh->disconnect();
		return $result;
	}else{
		if($params->param('searchString') && $params->param('searchString') ne ''){
			$json_data = fetch_data($dbh,$params->param('searchString'));
		}else{
			$json_data = fetch_data($dbh);
		}
		print $q->header(-type => "application/json", -charset => "utf-8");
		print encode_json($json_data);
    }
    $dbh->disconnect();
}

sub show_table {
my $show_status = shift;
print "Content-type: text/html\n\n";
print <<ENDHTML;
<html>
<head>
  <script data-require="jquery@*" data-semver="2.2.0" src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>
  <script src="http://code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
  <link rel="stylesheet" href="style.css" />
  <link href="http://code.jquery.com/ui/1.10.4/themes/ui-lightness/jquery-ui.css" rel="stylesheet">
  <script src="script.js"></script>
</head>

<body>
    <h1>Appointments</h1>
    <input type="button" id="new" name="add" value="New" onClick="addForm()" />	
    <input type="button" id="cancel" value="Cancel" onClick="hideAddForm()" />
    <div id="add_form">
	  <form id="appointmentForm" method="post" action="/index.cgi">
	  <input type="hidden" name="submitForm" value="submitForm"/>
      <div><label>DATE</label>
        <input type="text" name="date" placeholder="MM/DD/YYYY" id="date" /> 
		<span id="date-error" class="error"></span>
	  </div>
      <div><label>TIME</label>
        <input type="text" name="time" placeholder="HH:MM" id="time" />
		<span id="time-error" class="error"></span>
	  </div>
      <div><label>DESC</label>
        <textarea id="desc" name="desc" maxlength="500"></textarea>
      </div>
	  </form>
    </div>
    <div>
      <input type="text" id="query_str" />
      <input type="button" value="Search" id="search"/>
    </div>
    <div>	
	  <span class="info"></span>
      <table id="appointmentTable" style="display:none">
        <tr>
          <th>DATE</th>
          <th>TIME</th>
          <th>DESCRIPTION</th>
        </tr>
      </table>
    </div>
</body>
</html>
ENDHTML
}

sub parse_date {
    my $date_time = shift;
    my @date_time_array = split(' ',$date_time);
    my $time = $date_time_array[1];
	my $date = $date_time_array[0];
    return ($date,$time);
}

sub time_format {
	my $time = shift;
	my $change_12to24h = shift;
	my $format_time = $time;
	if($change_12to24h){
		if($time =~ m/(\d{1,2}):(\d{2}).*(am|pm|AM|PM)/){
			my $hh = $1;
			my $mm = $2;
			$hh -= 12 if ($3 =~ /am/i && $hh == 12);
			$hh += 12 if ($3 =~ /pm/i && $hh != 12);
			$hh = sprintf "%2d", $hh;
			$format_time = sprintf("%02d:%02d",$hh,$mm);
		}
	}else{
		if($time =~ m/(\d{1,2}):(\d\d)/){
			my $hh = $1;
			my $mm = $2;
			my $t = 'PM';
			$t = 'AM' if($1 == 12);
			$t = 'AM' if($1 < 12);
			$hh = $1 - 12 if($1 > 12);
			$format_time = sprintf("%02d:%02d %s",$hh,$mm,$t);
		}
	}
	return $format_time;
}

sub date_format {
	my $date = shift;
	my $format_date = shift;
	if($date =~ m/(\d{2})\/(\d{2})\/(\d{4})/){
		my $month = $months[$1-1];
		$format_date = $month." ".$2.","." ".$3;
	}
	return $format_date;
}
