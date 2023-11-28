import { lazy, useState } from 'react';
import { Navigate, useRoutes } from 'react-router-dom';

import demoData from 'src/utils/temp.json';

import DashboardLayout from 'src/layouts/dashboard';

export const IndexPage = lazy(() => import('src/pages/app'));
export const BlogPage = lazy(() => import('src/pages/blog'));
export const UserPage = lazy(() => import('src/pages/user'));
export const LoginPage = lazy(() => import('src/pages/login'));
export const ProductsPage = lazy(() => import('src/pages/products'));
export const Page404 = lazy(() => import('src/pages/page-not-found'));

// ----------------------------------------------------------------------

export default function Router() {
  const [search, setSearch] = useState('');
  const [date, setDate] = useState(''); // store date in YYYY-MM-DD format
  const [granularity, setGranularity] = useState('Month'); // store granularity in 'Month' or 'Day' format
  const [data, setData] = useState([]);

  const onSearch = (value) => {
    setSearch(value);
    getData(value, date, granularity);
  };

  const onChangeDate = (value) => {
    const formattedDate = value.toISOString().split('T')[0];
    setDate(formattedDate);
    getData(search, formattedDate, granularity);
  };

  const onChangeGranularity = (value) => {
    setGranularity(value);
    getData(search, date, value);
  };

  const getData = (currSearch, currDate, currGranularity) => {
    // based on 'date' and 'search' fetch data from backend
    console.log(`fetching data for: ${currDate} ${currSearch} ${currGranularity}`);
    const currDateTime = new Date(currDate);

    // filter all entries that match the currDateTime
    const newData = demoData.filter((item) => {
      const itemDateTime = new Date(item.Date);
      if (currGranularity === 'Month') {
        return (
          itemDateTime.getFullYear() === currDateTime.getFullYear() &&
          itemDateTime.getMonth() === currDateTime.getMonth()
        );
      }
      return (
        itemDateTime.getFullYear() === currDateTime.getFullYear() &&
        itemDateTime.getMonth() === currDateTime.getMonth() &&
        itemDateTime.getDate() === currDateTime.getDate()
      );
    });
    
    // add tag for granularity
    newData.granularity = currGranularity;

    // wrap sent_label in array
    newData.forEach((item) => {
      item.sent_labels = [item.sent_label];
    });

    // if granularity is 'Month' then take aggregate per day
    if (currGranularity === 'Month') {
      const newDataPerDay = {};
      newData.forEach((item) => {
        const itemDateTime = new Date(item.Date);
        const itemDate = itemDateTime.getDate();
        if (itemDate in newDataPerDay) {
          newDataPerDay[itemDate].Volume += item.Volume;
          newDataPerDay[itemDate].Low = Math.min(newDataPerDay[itemDate].Low, item.Low);
          newDataPerDay[itemDate].High = Math.max(newDataPerDay[itemDate].High, item.High);

          // add sent_label to array
          newDataPerDay[itemDate].sent_labels.push(item.sent_label);

          // {
          //   "stock": "AAPL",
          //   "Date": "2016-01-04 09:00:00",
          //   "Open": 98.7787,
          //   "High": 98.7955,
          //   "Low": 98.7765,
          //   "Close": 98.7933,
          //   "Volume": 945459,
          //   "OpenInt": 0,
          //   "better_pos": 0.143,
          //   "better_neg": 0.033,
          //   "better_neutral": 0.824,
          //   "sent_label": "pos",
          //   "cumulative_sent": 66.9158213205
          // },
        } else {
          newDataPerDay[itemDate] = {
            Date: item.Date,
            Volume: item.Volume,
            Low: item.Low,
            High: item.High,
            sent_labels: [],
          };
        }
      });
      const newDataPerDayArray = Object.values(newDataPerDay);
      setData(newDataPerDayArray);
      return;
    }
    setData(newData);
  };

  const routes = useRoutes([
    {
      element: (
        <DashboardLayout
          onSearch={onSearch}
          onChangeDate={onChangeDate}
          onChangeGranularity={onChangeGranularity}
        >
          <IndexPage data={data} />
        </DashboardLayout>
      ),
      index: true,
      // children: [
      //   { element: <IndexPage />, index: true },
      //   { path: 'user', element: <UserPage /> },
      //   { path: 'products', element: <ProductsPage /> },
      //   { path: 'blog', element: <BlogPage /> },
      // ],
    },
    {
      path: 'login',
      element: <LoginPage />,
    },
    {
      path: '404',
      element: <Page404 />,
    },
    {
      path: '*',
      element: <Navigate to="/404" replace />,
    },
  ]);

  return routes;
}
