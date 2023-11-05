# pie
i gave up on my most recent project i started 10 minutes ago so here's an attempt to make a developer environment that i will give up on in the next 10 mintues probably

## making crusts
Crusts are what actually "compile" (or package or whatever) Pie projects. They are organized like so:
`<tld>.<domain name>.<crust name>`

So for Playdate, who's domain is at `play.date`, it's named like this:
`date.play.playdate_pie`

From there's one more submodule, which is the platform. i.e., `date.play.playdate_pie.playdate`. 