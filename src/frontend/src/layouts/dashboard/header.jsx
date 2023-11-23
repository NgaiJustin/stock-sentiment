// import PropTypes from 'prop-types';
import { useState } from 'react';

import Box from '@mui/material/Box';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import { useTheme } from '@mui/material/styles';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';

import { useResponsive } from 'src/hooks/use-responsive';

import { bgBlur } from 'src/theme/css';

// import Iconify from 'src/components/iconify';

import { HEADER } from './config-layout';
import Searchbar from './common/searchbar';

// ----------------------------------------------------------------------

export default function Header() {
  const [query, setQuery] = useState('');

  const theme = useTheme();

  const lgUp = useResponsive('up', 'lg');

  const renderContent = (
    <>
      <Searchbar
        value={query}
        onChange={(event) => {
          setQuery(event.target.value);
        }}
        onSearch={() => {
          console.log(`Searched: ${query}`);
        }}
      />

      <Box sx={{ flexGrow: 1 }} />

      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DatePicker
          onAccept={(date) => {
            console.log(date);
          }}
        />
      </LocalizationProvider>
    </>
  );

  return (
    <AppBar
      sx={{
        boxShadow: 'none',
        height: HEADER.H_MOBILE,
        zIndex: theme.zIndex.appBar + 1,
        ...bgBlur({
          color: theme.palette.background.default,
        }),
        transition: theme.transitions.create(['height'], {
          duration: theme.transitions.duration.shorter,
        }),
        ...(lgUp && {
          width: `calc(100%)`,
          height: HEADER.H_DESKTOP,
        }),
      }}
    >
      <Toolbar
        sx={{
          height: 1,
          px: { lg: 5 },
        }}
      >
        {renderContent}
      </Toolbar>
    </AppBar>
  );
}

// Header.propTypes = {
//   onOpenNav: PropTypes.func,
// };
