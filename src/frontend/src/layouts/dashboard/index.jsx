// import { useState } from 'react';
import { Suspense } from 'react';
import PropTypes from 'prop-types';

import Box from '@mui/material/Box';

// import Nav from './nav';
import Main from './main';
import Header from './header';

// ----------------------------------------------------------------------

export default function DashboardLayout({onSearch, onChangeDate, onChangeGranularity, children }) {
  // const [openNav, setOpenNav] = useState(false);
  return (
    <>
      <Header
        onSearch={onSearch}
        onChangeDate={onChangeDate}
        onChangeGranularity={onChangeGranularity}
      />
      <Box
        sx={{
          minHeight: 1,
          display: 'flex',
          flexDirection: { xs: 'column', lg: 'row' },
        }}
      >
        <Suspense>
          <Main>{children}</Main>
        </Suspense>
      </Box>
    </>
  );
}

DashboardLayout.propTypes = {
  onSearch: PropTypes.func,
  onChangeDate: PropTypes.func,
  onChangeGranularity: PropTypes.func,
  children: PropTypes.node,
};
