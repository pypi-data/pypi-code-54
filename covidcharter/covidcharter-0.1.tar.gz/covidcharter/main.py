import click
from covidcharter.service import filter_by_county, plot_data, get_all_counties


@click.command()
@click.option('--county', help='The county or locality to get the graph for')
def graph(county):
    try:
        click.echo('Graphing the data...')
        df = filter_by_county(county)
        plot_data(df)
    except:
        counties = get_all_counties()
        click.echo('Please try again. The covidcharter data chart generator requires a county from the following list: %s'
                   % counties)


if __name__ == '__main__':
    graph()
