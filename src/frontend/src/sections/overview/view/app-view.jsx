import PropTypes from 'prop-types';
import { faker } from '@faker-js/faker';

import Container from '@mui/material/Container';
import Grid from '@mui/material/Unstable_Grid2';
import Typography from '@mui/material/Typography';

// import Iconify from 'src/components/iconify';
import { fShortenNumber } from 'src/utils/format-number';

// import AppTasks from '../app-tasks';
import AppNewsUpdate from '../app-news-update';
// import AppOrderTimeline from '../app-order-timeline';
import AppCurrentVisits from '../app-current-visits';
import AppWebsiteVisits from '../app-website-visits';
import AppWidgetSummary from '../app-widget-summary';
// import AppTrafficBySite from '../app-traffic-by-site';
// import AppCurrentSubject from '../app-current-subject';
import AppConversionRates from '../app-conversion-rates';

// ----------------------------------------------------------------------

export default function AppView({ data }) {
  // Price information
  const firstOpen = data.length > 0 ? data[0].Open : 0;
  const lastClose = data.length > 0 ? data[data.length - 1].Close : 0;
  const change = lastClose - firstOpen;
  const percentChange = (change / firstOpen) * 100;
  const formattedPercentChange = `${percentChange > 0 ? '+' : ''}${percentChange.toFixed(2)}%`;

  // Volume information
  // group by hour if granularity is day
  const entriesGroup =
    data.granularity === 'Day'
      ? Array.from(
          data
            .filter((item) => item.Date.length > 10) // filter out items with no time
            .map((item) => ({
              ...item,
              Date: item.Date.substring(0, 13), // group by hour
            }))
            .reduce(
              (entryMap, e) =>
                // group by hour
                entryMap.set(e.Date, [...(entryMap.get(e.Date) || []), e]),
              new Map()
            )
        ).map((item) => ({
          Date: item[0],
          Volume: item[1].reduce((acc, curr) => acc + curr.Volume, 0),
        }))
      : data;

  const volumeSeries = entriesGroup
    .map((item) => ({
      label: item.Date.substring(0, data.granularity === 'Day' ? 13 : 10) || 'N/A',
      value: item.Volume || 0,
    }))
    .filter((item) => item.label !== 'N/A')
    .filter((item) => item.value !== 0)
    .map((item) => ({
      label: item.label + (data.granularity === 'Day' ? ':00' : ''),
      value: item.value,
    }));

  const totalTradeVolume = volumeSeries.reduce((acc, curr) => acc + curr.value, 0);

  // News information
  const newsSeries =
    data.length > 0
      ? [...Array(5)].map((_, index) => ({
          id: faker.string.uuid(),
          title: data[data.length - 1 - index][`title_${index + 1}`],
          description: data[data.length - 1 - index][`text_${index + 1}`],
          image: `/assets/images/covers/cover_${index + 1}.jpg`,
          postedAt: faker.date.recent(),
        }))
      : [];

  

  return (
    <Container maxWidth="xl">
      <Typography variant="h4" sx={{ mb: 5 }}>
        Hi, Welcome back 👋
      </Typography>

      <Grid container spacing={3}>
        <Grid xs={12} sm={6} md={3}>
          <AppWidgetSummary
            title="Total Volume"
            total={data.reduce((acc, curr) => acc + curr.Volume, 0)}
            color="success"
            format={fShortenNumber}
            icon={<img alt="icon" src="/assets/icons/glass/ic_glass_buy.png" />}
          />
        </Grid>

        <Grid xs={12} sm={6} md={3}>
          <AppWidgetSummary
            title="Average Price"
            total={data.reduce((acc, curr) => acc + (curr.Low + curr.High) / 2, 0) / data.length}
            color="info"
            icon={<img alt="icon" src="/assets/icons/glass/ic_glass_bag.png" />}
          />
        </Grid>

        <Grid xs={12} sm={6} md={3}>
          <AppWidgetSummary
            title="Low"
            total={
              data.length > 0 ? data.reduce((acc, curr) => Math.min(acc, curr.Low), Infinity) : 0
            }
            color="warning"
            icon={<img alt="icon" src="/assets/icons/glass/low.png" />}
          />
        </Grid>

        <Grid xs={12} sm={6} md={3}>
          <AppWidgetSummary
            title="High"
            total={
              data.length > 0 ? data.reduce((acc, curr) => Math.max(acc, curr.High), -Infinity) : 0
            }
            color="error"
            icon={<img alt="icon" src="/assets/icons/glass/high.png" />}
          />
        </Grid>

        <Grid xs={12} md={6} lg={8}>
          <AppWebsiteVisits
            title="Price Chart"
            subheader={`(${formattedPercentChange}) from last closure`}
            chart={{
              labels: data.map((item) => item.Date),
              series: [
                // {
                //   name: 'Volume',
                //   type: 'column',
                //   fill: 'solid',
                //   data: data.map((item) => item.Volume),
                // },
                {
                  name: 'Price',
                  type: 'area',
                  fill: 'gradient',
                  color: `${change > 0 ? '#2DCE89' : '#F5365C'}`,
                  // Round to 4 decimal places
                  data: data.map(
                    (item) => Math.round(((item.Low + item.High) / 2) * 10000) / 10000
                  ),
                },
              ],
            }}
          />
        </Grid>

        <Grid xs={12} md={6} lg={4}>
          <AppCurrentVisits
            title="Sentiment"
            chart={{
              series: [
                {
                  label: 'Positive',
                  value: data.reduce(
                    (acc, curr) => acc + curr.sent_labels.filter((x) => x === 'pos').length,
                    0
                  ),
                },
                {
                  label: 'Negative',
                  value: data.reduce(
                    (acc, curr) => acc + curr.sent_labels.filter((x) => x === 'neg').length,
                    0
                  ),
                },
                {
                  label: 'Neutral',
                  value: data.reduce(
                    (acc, curr) => acc + curr.sent_labels.filter((x) => x === 'neutral').length,
                    0
                  ),
                },
                {
                  label: 'Risky',
                  value: data.reduce(
                    (acc, curr) => acc + curr.sent_labels.filter((x) => x === 'risky').length,
                    0
                  ),
                },
              ],
            }}
          />
        </Grid>

        <Grid xs={12} md={6} lg={8}>
          <AppConversionRates
            title="Trade Volumes"
            subheader={`Total Volume: ${fShortenNumber(totalTradeVolume)}`}
            chart={{
              series: volumeSeries,
            }}
          />
        </Grid>

        {/* <Grid xs={12} md={6} lg={4}>
          <AppCurrentSubject
            title="Current Subject"
            chart={{
              categories: ['English', 'History', 'Physics', 'Geography', 'Chinese', 'Math'],
              series: [
                { name: 'Series 1', data: [80, 50, 30, 40, 100, 20] },
                { name: 'Series 2', data: [20, 30, 40, 80, 20, 80] },
                { name: 'Series 3', data: [44, 76, 78, 13, 43, 10] },
              ],
            }}
          />
        </Grid> */}

        <Grid xs={12} md={6} lg={4}>
          <AppNewsUpdate title="News Update" list={newsSeries} />
        </Grid>

        {/* <Grid xs={12} md={6} lg={4}>
          <AppOrderTimeline
            title="Order Timeline"
            list={[...Array(5)].map((_, index) => ({
              id: faker.string.uuid(),
              title: [
                '1983, orders, $4220',
                '12 Invoices have been paid',
                'Order #37745 from September',
                'New order placed #XF-2356',
                'New order placed #XF-2346',
              ][index],
              type: `order${index + 1}`,
              time: faker.date.past(),
            }))}
          />
        </Grid> */}
      </Grid>
    </Container>
  );
}

AppView.propTypes = {
  data: PropTypes.object,
};
