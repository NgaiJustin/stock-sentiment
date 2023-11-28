import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet-async';

import { AppView } from 'src/sections/overview/view';

// ----------------------------------------------------------------------

export default function AppPage({data}) {
  return (
    <>
      <Helmet>
        <title> Dashboard | Minimal UI </title>
      </Helmet>

      <AppView data={data} />
    </>
  );
}

AppPage.propTypes = {
  data: PropTypes.array,
};